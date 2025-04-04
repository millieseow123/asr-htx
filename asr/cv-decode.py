import pandas as pd
import requests
import os
from tqdm import tqdm

# Paths
BASE_DIR = "/Users/millieseow/Downloads/common_voice"
CSV_PATH = os.path.join(BASE_DIR, "cv-valid-dev.csv")
AUDIO_DIR = os.path.join(BASE_DIR, "cv-valid-dev")
API_URL = "http://localhost:8001/asr"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Add new column for generated text
generated_texts = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    file_path = os.path.join(AUDIO_DIR, row["filename"])
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(API_URL, files=files)
            result = response.json()
            generated_texts.append(result.get("transcription", ""))
    except Exception as e:
        print(f"Error with file {file_path}: {e}")
        generated_texts.append("")

df["generated_text"] = generated_texts

# Save the updated CSV
df.to_csv(os.path.join(BASE_DIR, "cv-valid-dev-transcribed.csv"), index=False)
print("✅ Transcription complete! Output saved.")
