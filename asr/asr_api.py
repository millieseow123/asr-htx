from flask import Flask, request, jsonify
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import os
from pydub import AudioSegment
import librosa
import uuid

app = Flask(__name__)

# Load tokenizer and model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/asr", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files["file"]
    filename = f"temp_{uuid.uuid4()}.wav"

    # Convert MP3 to WAV (16kHz mono)
    try:
        sound = AudioSegment.from_file(audio_file, format="mp3")
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(filename, format="wav")

        # Load audio
        input_audio, sample_rate = librosa.load(filename, sr=16000)

        input_values = tokenizer(input_audio, return_tensors="pt", padding="longest").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.decode(predicted_ids[0])

        # Get duration
        duration = librosa.get_duration(y=input_audio, sr=sample_rate)

        os.remove(filename)  # Clean up temp file

        return jsonify({
            "transcription": transcription,
            "duration": f"{duration:.2f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
