## Project Structure

- `asr/`: ASR microservice with wav2vec2 model
- `deployment-design/`: Architecture design (PDF)
- `elastic-backend/`: Elasticsearch indexing setup
- `search-ui/`: Frontend search interface

## Run ASR API with Docker

1. Build the image:
```bash
    docker build -t asr-api ./asr
```
2. Run the container:
```bash
    docker run -p 8001:8001 asr-api
```
3. Test the API:
```bash
    curl -F "file=@/path/to/sample.mp3" http://localhost:8001/asr
```
