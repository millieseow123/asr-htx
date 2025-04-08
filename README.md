A searchable audio transcript interface using Wav2Vec2, Elasticsearch, Flask, and React.

URL: [http://3.90.182.103/](http://3.90.182.103/)

## Project Structure

- `asr/`: ASR microservice with wav2vec2 model
- `deployment-design/`: Architecture design (PDF)
- `elastic-backend/`: Elasticsearch indexing setup
- `search-ui/`: Frontend search interface


## Run ASR API with Docker
1. Navigate to directory
```bash 
cd asr
```
2. Build the image:
```bash
docker build -t asr-api ./asr
```
3. Run the container:
```bash
docker run -p 8001:8001 asr-api
```
4. Test the API:
```bash
curl -F "file=@/path/to/sample.mp3" http://localhost:8001/asr
```

## Run Elasticsearch Backend
1. Navigate to directory
```bash 
cd elastic-backend
```

2. (Optional but recommended) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start Elasticsearch cluster
```bash
docker compose up
```
Open [http://localhost:9200/_cat/nodes?v](http://localhost:9200/_cat/nodes?v) in your browser — you should see both es01 and es02 nodes listed.

5. Index data
```bash
python cv-index.py
```

6. Start backend API server
```bash
python search_api.py
```

## Run Frontend (search-ui)

1. Navigate to the frontend directory:
```bash
cd search-ui
```

2. Install dependencies:
```bash
npm install
```

3. Start development sever
```bash
npm start
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Limitations

- The ASR model used (`wav2vec2-large-960h`) may produce inaccurate transcriptions, especially for non-US accents or noisy audio, therefore the search function searches both transcribed and actual audio
- Some metadata fields (e.g., age, gender, accent) may be missing or inconsistent in the source CSV file.
- The search UI currently does not support fuzzy matching or partial phrase queries.
- Facets are limited to a fixed number of values (e.g., only top 10 accent types are shown).
- Backend and search functionality assumes the local Elasticsearch and ASR services are running on ports `9200` and `8001` respectively.
