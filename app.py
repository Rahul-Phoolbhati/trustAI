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
from googleapiclient import discovery

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Google API
API_KEY = 'AIzaSyAsXyKV32H990ll4npotKQtx4JGYRWe_8M'
perspective_client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

def check_harmful_content(text):
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'THREAT': {},
            'PROFANITY': {}
        }
    }
    
    try:
        response = perspective_client.comments().analyze(body=analyze_request).execute()
        
        # Check if any attribute score is above threshold (0.7)
        threshold = 0.7
        for attribute, scores in response['attributeScores'].items():
            if scores['summaryScore']['value'] > threshold:
                return True, attribute
        
        return False, None
    except Exception as e:
        print(f"Error checking content: {e}")
        return False, None

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

        if not current_recording or not os.path.exists(current_recording):
            return jsonify({'error': 'No recording available'}), 400

        # Add voice to database
        add_friend(voice_db, name, current_recording)
        return jsonify({'success': f'Voice added successfully for {name}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/match_voice', methods=['POST'])
def match_voice_route():
    try:
        if not current_recording or not os.path.exists(current_recording):
            return jsonify({'error': 'No recording available'}), 400

        # Match the voice
        result = match_voice(current_recording)
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect_ai', methods=['POST'])
def detect_ai():
    try:
        if not current_recording or not os.path.exists(current_recording):
            return jsonify({'error': 'No recording available'}), 400

        # Analyze if the voice is AI or real
        result = analyze_audio(current_recording)
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    

if __name__ == '__main__':
    app.run(debug=True)