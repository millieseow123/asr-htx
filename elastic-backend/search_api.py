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
    
    # Searches both transcribed and actual audio
    if "generated_text" in request.args and request.args["generated_text"].strip():
        query["bool"]["must"].append({
            "multi_match": {
                "query": request.args["generated_text"],
                "fields": ["generated_text", "text"]
            }
        })

    # Filters
    for field in ["duration", "age", "gender", "accent"]:
        if field in request.args:
            query["bool"]["filter"].append({
                "term": {field: request.args[field]}
            })
    
    aggs = {
            "age_values": {"terms": {"field": "age", "size": 9,  "min_doc_count": 0 }},
            "gender_values": {"terms": {"field": "gender", "size": 3, "min_doc_count": 0 }},
            "accent_values": {"terms": {"field": "accent", "size": 16 , "min_doc_count": 0 }},
            "duration_values": {
            "range": {
                "field": "duration",
                "ranges": [
                    {"to": 2, "key": "Very short (0–2s)"},
                    {"from": 2, "to": 4, "key": "Short (2–4s)"},
                    {"from": 4, "to": 6, "key": "Medium (4–6s)"},
                    {"from": 6, "to": 8, "key": "Long (6–8s)"},
                    {"from": 8, "key": "Very long (8s+)"}
                ]
            }
        }
    }
    results_per_page = int(request.args.get("resultsPerPage", 10))

    res = es.search(index="cv-valid-dev-transcribed", query=query, aggs=aggs, size=results_per_page)

    # Extract hits
    results = res["hits"]["hits"]

    # Format facets
    def format_facet(name, buckets, type="value"):
        return [{
            "field": name,
            "type": type,
            "data": [{"value": b["key"], "count": b["doc_count"]} for b in buckets]
        }]

    facets = {
        "age": format_facet("age", res["aggregations"]["age_values"]["buckets"]),
        "gender": format_facet("gender", res["aggregations"]["gender_values"]["buckets"]),
        "accent": format_facet("accent", res["aggregations"]["accent_values"]["buckets"]),
        "duration": format_facet("duration", res["aggregations"]["duration_values"]["buckets"]),
    }

    return jsonify({
        "results": results,
        "facets": facets
    })

if __name__ == "__main__":
    app.run(port=8002)
