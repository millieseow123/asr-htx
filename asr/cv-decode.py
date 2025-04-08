import pandas as pd
import requests
import os
from pydub import AudioSegment
from tqdm import tqdm

BASE_DIR = "/Users/millieseow/Downloads/common_voice"
CSV_PATH = os.path.join(BASE_DIR, "cv-valid-dev.csv")
AUDIO_DIR = os.path.join(BASE_DIR, "cv-valid-dev", "cv-valid-dev")
API_URL = "http://localhost:8001/asr"

df = pd.read_csv(CSV_PATH)

durations = []
generated_texts = []

for filename in tqdm(df["filename"]):
    try:
        mp3_file = filename.split("/")[-1]  
        audio_path = os.path.join(AUDIO_DIR, mp3_file)

        # Get audio duration
        audio = AudioSegment.from_file(audio_path)
        duration_sec = len(audio) / 1000.0
        durations.append(duration_sec)

        # Send audio to ASR service
        with open(audio_path, "rb") as f:
            response = requests.post(API_URL, files={"file": f})
        if response.status_code == 200:
            transcript = response.json().get("transcription", "")
            generated_texts.append(transcript)

        else:
            print(f"❌ ASR error for {mp3_file}: {response.status_code} - {response.text}")
            generated_texts.append("")

    except Exception as e:
        print(f"⚠️ Error reading {filename}: {e}")
        durations.append(None)
        generated_texts.append("")

df["duration"] = durations
df["generated_text"] = generated_texts


df.to_csv(os.path.join(BASE_DIR, "cv-valid-dev-transcribed-10rows.csv"), index=False)
print("✅ Transcription complete! Output saved.")
