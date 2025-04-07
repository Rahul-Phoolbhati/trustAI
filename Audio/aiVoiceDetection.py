# import torch
# from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor
# import torchaudio

# # Load model and processor
# model_name = "Mrkomiljon/voiceGUARD"
# model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
# processor = Wav2Vec2Processor.from_pretrained(model_name)

# # Load audio
# waveform, sample_rate = torchaudio.load("./newtest.wav")

# # Resample if necessary
# if sample_rate != 16000:
#     resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
#     waveform = resampler(waveform)

# # Preprocess
# inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding=True)

# # Inference
# with torch.no_grad():
#     logits = model(**inputs).logits
#     predicted_ids = torch.argmax(logits, dim=-1)

# print(predicted_ids.item())

# # Map to label
# labels = ["Real Human Voice", "AI-generated"]
# prediction = labels[predicted_ids.item()]
# print(f"Prediction: {prediction}")
