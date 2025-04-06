# import pyaudio

# def record_audio(duration=5, sample_rate=16000):
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
#     frames = []

#     for _ in range(0, int(sample_rate / 1024 * duration)):
#         data = stream.read(1024)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#     return b''.join(frames)

# a = record_audio()
# print(a)



# import pyaudio
# import wave
# import numpy as np

# def record_audio(duration=5, sample_rate=16000, filename="output.wav"):
#     audio = pyaudio.PyAudio()
    
#     # Open audio stream for recording
#     stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
#     frames = []

#     # Record audio
#     print("Recording...")
#     for _ in range(0, int(sample_rate / 1024 * duration)):
#         data = stream.read(1024)
#         frames.append(data)

#     # Stop the stream
#     print("Recording finished.")
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     # Save the recorded data to a WAV file
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
#         wf.setframerate(sample_rate)
#         wf.writeframes(b''.join(frames))

#     # Optionally, play back the audio after recording
#     print("Playing back the recorded audio...")
#     playback_audio(filename)

# def playback_audio(filename):
#     # Play back the recorded WAV file
#     import simpleaudio as sa
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     wave_obj.play()

# # Call the function to start recording
# record_audio(duration=5, sample_rate=16000)

import pyaudio
import wave

def record_audio(duration=20, sample_rate=16000, filename="output.wav"):
    audio = pyaudio.PyAudio()

    # Open audio stream for recording
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"Saved to {filename}")
    # playback_audio(filename)

def playback_audio(filename):
    # Play back the recorded WAV file using PyAudio
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    # Open a stream to play back the audio
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=wf.getframerate(),
                        output=True)

    # Read and play the audio in chunks
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Close the stream after playback
    stream.stop_stream()
    stream.close()
    audio.terminate()

# # Call the function to start recording
# record_audio(duration=10, sample_rate=16000, filename="newtest.wav")
