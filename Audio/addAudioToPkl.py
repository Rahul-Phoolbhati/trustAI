import librosa
import numpy as np
import pickle
from resemblyzer import VoiceEncoder, preprocess_wav
from Audio.record import record_audio


from transformers import Wav2Vec2Processor, Wav2Vec2Model
import torch

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")

def extract_voice_embedding_from_Ptnd(audio_file):
    y, sr = librosa.load(audio_file, sr=16000)
    input_values = processor(y, return_tensors="pt", sampling_rate=sr).input_values
    with torch.no_grad():
        embeddings = model(input_values).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

# Function to extract features
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfccs, axis=1)


encoder = VoiceEncoder()
def extract_voice_embedding(audio_file):
    wav = preprocess_wav(audio_file)
    return encoder.embed_utterance(wav)

# Add a new record for a friend
def add_friend(voice_db, friend_name, audio_file):
    features = extract_voice_embedding(audio_file)
    voice_db[friend_name] = features

    # Save the updated dictionary
    with open("voice_database.pkl", "wb") as f:
        pickle.dump(voice_db, f)

# Load the existing voice database
voice_db={}
with open("/Users/rahulphoolbhati/GDG/Audio/voice_database.pkl", "rb") as f:
    voice_db = pickle.load(f)

# Add a new friend's voice
# record_audio()
# add_friend(voice_db, "parkhi", "output.wav")

# print("New friend's voice added successfully!")
