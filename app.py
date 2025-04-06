import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from predict import analyze_audio
from Audio.match import match_voice
from Audio.addAudioToPkl import add_friend, voice_db
from Audio.record import record_audio, playback_audio
import threading
import time
import signal
from HarmContentDetection import check_harmful_content
from chatbot import ansTheQuery

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables for recording state
recording_thread = None
is_recording = False
current_recording = None

def stop_recording_signal(signum, frame):
    global is_recording
    is_recording = False

signal.signal(signal.SIGINT, stop_recording_signal)

def record_audio_thread():
    global is_recording
    try:
        record_audio()
    except Exception as e:
        print(f"Recording error: {e}")
    finally:
        is_recording = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_query', methods=['POST'])
def check_query():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        is_harmful, attribute = check_harmful_content(text)
        
        if is_harmful:
            return jsonify({
                'error': 'Cannot process this query',
                'reason': f'Content flagged as potentially {attribute.lower()}'
            }), 400
        
        return jsonify({'success': True, 'message': 'Query is safe to process'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording_thread, is_recording
    if not is_recording:
        is_recording = True
        recording_thread = threading.Thread(target=record_audio_thread)
        recording_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        recording_thread.start()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Recording already in progress'}), 400

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording_thread, is_recording, current_recording
    if is_recording:
        is_recording = False
        if recording_thread and recording_thread.is_alive():
            recording_thread.join(timeout=1.0)  # Wait for thread to finish with timeout
        current_recording = "output.wav"
        if os.path.exists(current_recording):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Recording failed to save'}), 500
    return jsonify({'error': 'No recording in progress'}), 400

@app.route('/add_voice', methods=['POST'])
def add_voice():
    try:
        name = request.form.get('name')
        if not name:
            return jsonify({'error': 'No name provided'}), 400

        file_path = None
        
        # Check if file was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        # Otherwise use the recorded file
        elif current_recording and os.path.exists(current_recording):
            file_path = current_recording
        else:
            return jsonify({'error': 'No audio file provided'}), 400

        # Add voice to database
        add_friend(voice_db, name, file_path)
        
        # Clean up the file if it was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            os.remove(file_path)
            
        return jsonify({'success': f'Voice added successfully for {name}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/match_voice', methods=['POST'])
def match_voice_route():
    try:
        file_path = None
        
        # Check if file was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        # Otherwise use the recorded file
        elif current_recording and os.path.exists(current_recording):
            file_path = current_recording
        else:
            return jsonify({'error': 'No audio file provided'}), 400

        # Match the voice
        result = match_voice(file_path)
        
        # Clean up the file if it was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            os.remove(file_path)
            
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect_ai', methods=['POST'])
def detect_ai():
    try:
        file_path = None
        
        # Check if file was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        # Otherwise use the recorded file
        elif current_recording and os.path.exists(current_recording):
            file_path = current_recording
        else:
            return jsonify({'error': 'No audio file provided'}), 400

        # Analyze if the voice is AI or real
        result = analyze_audio(file_path)
        
        # Clean up the file if it was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            os.remove(file_path)
            
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat')
def chat():
    query = request.args.get('query', '')
    return render_template('chat.html', initial_query=query)

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        # Get response from AI
        response = ansTheQuery(data['text'])
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    

if __name__ == '__main__':
    app.run(debug=True)