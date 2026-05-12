from flask import Flask, jsonify
import os
import socket
import redis
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# PrometheusMetrics automatically creates /metrics endpoint
# No need to define it manually!
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info',
             version=os.environ.get('APP_VERSION', '1.0'),
             environment=os.environ.get('APP_ENV', 'development'))

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )

@app.route("/")
def hello():
    try:
        r = get_redis()
        visits = r.incr("visit_counter")
        redis_status = "Connected ✅"
    except Exception as e:
        visits = "Redis unavailable"
        redis_status = f"Error: {str(e)}"

    app_env = os.environ.get("APP_ENV", "not-set")
    app_version = os.environ.get("APP_VERSION", "not-set")

    return """
    <html>
        <body style="font-family: Arial; margin: 40px; background: #f0f0f0;">
            <h1>🚀 Hello from Kubernetes!</h1>
            <h2>📦 Pod Info</h2>
            <p>Pod Name: <b>{}</b></p>
            <p>Pod IP: <b>{}</b></p>
            <h2>🔢 Visit Counter</h2>
            <p>Total Visits: <b>{}</b></p>
            <p>Redis Status: <b>{}</b></p>
            <h2>⚙️ Config</h2>
            <p>Environment: <b>{}</b></p>
            <p>Version: <b>{}</b></p>
        </body>
    </html>
    """.format(
        os.environ.get("HOSTNAME", "unknown"),
        socket.gethostbyname(socket.gethostname()),
        visits,
        redis_status,
        app_env,
        app_version
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

# ← NO /metrics route here!
# PrometheusMetrics handles it automatically ✅

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=False)