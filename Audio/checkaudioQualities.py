import librosa

y, sr = librosa.load("your_voice_enroll.wav", sr=16000)
print(f"Enroll duration: {len(y)/sr:.2f} sec")

y2, sr = librosa.load("your_voice_test_different_words.wav", sr=16000)
print(f"Test duration: {len(y2)/sr:.2f} sec")