from scipy.spatial.distance import cosine
import pickle
import os
from Audio.addAudioToPkl import extract_voice_embedding

def match_voice(incoming_audio):
    incoming_features = extract_voice_embedding(incoming_audio)
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "voice_database.pkl")
    with open(db_path, "rb") as f:
        voice_db = pickle.load(f)

    for name, stored_features in voice_db.items():
        similarity = 1 - cosine(stored_features, incoming_features)
        if similarity > 0.85:  # Threshold for matching
            return f"Verified: {name}'s voice detected with similarity = {similarity}"
        # else:
            # print(f"similarity = {similarity}")
    
    return "Unknown or AI-generated voice detected"

# Comment out the test code when used as a module
# from record import playback_audio, record_audio
# record_audio();
# result = match_voice("output.wav")
# print(result)
# playback_audio("./output.wav")