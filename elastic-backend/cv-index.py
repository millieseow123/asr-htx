from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch("http://localhost:9200")

# Delete existing index if needed
if es.indices.exists(index="cv-valid-dev-transcribed"):
    es.indices.delete(index="cv-valid-dev-transcribed")

# Create index with mappings
es.indices.create(
    index="cv-valid-dev-transcribed",
    body={
        "mappings": {
            "properties": {
                "filename": {"type": "keyword"},
                "generated_text": {"type": "text"},
                "duration": {"type": "float"},
                "age": {"type": "keyword"},
                "gender": {"type": "keyword"},
                "accent": {"type": "keyword"}
            }
        }
    }
)

# Load CSV
df = pd.read_csv("cv-valid-dev-transcribed.csv")

# Index rows
for _, row in df.iterrows():
    doc = {
        "filename": row["filename"],
        "generated_text": None if pd.isna(row["generated_text"]) else row["generated_text"],
        "duration": None if pd.isna(row.get("duration")) else row.get("duration"),
        "age": None if pd.isna(row.get("age")) else row.get("age"),
        "gender": None if pd.isna(row.get("gender")) else row.get("gender"),
        "accent": None if pd.isna(row.get("accent")) else row.get("accent")
    }
    es.index(index="cv-valid-dev-transcribed", document=doc)

print("✅ Indexing complete.")
