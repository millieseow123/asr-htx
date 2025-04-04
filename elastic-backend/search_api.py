from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app) 
es = Elasticsearch("http://localhost:9200")

@app.route("/search", methods=["GET"])
def search():
    query = {
        "bool": {
            "must": [],
            "filter": []
        }
    }

    # Full-text search
    if "generated_text" in request.args:
        query["bool"]["must"].append({
            "match": {
                "generated_text": request.args["generated_text"]
            }
        })

    # Filters
    for field in ["duration", "age", "gender", "accent"]:
        if field in request.args:
            query["bool"]["filter"].append({
                "term": {field: request.args[field]}
            })

    res = es.search(index="cv-valid-dev-transcribed", query=query)
    return jsonify(res["hits"]["hits"])

if __name__ == "__main__":
    app.run(port=8002)
