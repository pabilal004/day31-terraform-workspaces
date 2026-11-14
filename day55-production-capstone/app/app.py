import os
from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
UP = Gauge("app_up", "Application process health")
UP.set(1)

@app.before_request
def count_request():
    from flask import request, g
    g.started = True

@app.after_request
def record_request(response):
    from flask import request
    REQUESTS.labels(request.method, request.path, str(response.status_code)).inc()
    return response

@app.get("/")
def home():
    return jsonify(application="production-capstone", status="running",
                   environment=os.getenv("APP_ENV", "development"))

@app.get("/health")
def health():
    return jsonify(status="healthy"), 200

@app.get("/ready")
def ready():
    return jsonify(status="ready"), 200

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.errorhandler(404)
def not_found(_error):
    return jsonify(error="not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
