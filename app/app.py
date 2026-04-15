from flask import Flask, jsonify
import os
import socket
import redis

app = Flask(__name__)

# Redis connection — using headless service DNS
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-0.redis.default.svc.cluster.local")
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
        # Increment visit counter
        visits = r.incr("visit_counter")
        redis_status = "Connected ✅"
    except Exception as e:
        visits = "Redis unavailable"
        redis_status = f"Error: {str(e)}"

    # Get config from ConfigMap
    app_env = os.environ.get("APP_ENV", "not-set")
    app_version = os.environ.get("APP_VERSION", "not-set")

    # Get secrets
    db_password = os.environ.get("DB_PASSWORD", "not-set")

    # Read mounted config file
    config_file = "not-set"
    try:
        with open("/etc/properties/app.properties", "r") as f:
            config_file = f.read()
    except:
        config_file = "file not found"

    return """
    <html>
        <body style="font-family: Arial; margin: 40px; background: #f0f0f0;">
            <h1>🚀 Hello from Kubernetes!</h1>

            <h2>📦 Pod Info</h2>
            <p>Pod Name: <b>{}</b></p>
            <p>Pod IP: <b>{}</b></p>

            <h2>🔢 Visit Counter (stored in Redis)</h2>
            <p>Total Visits: <b>{}</b></p>
            <p>Redis Status: <b>{}</b></p>

            <h2>⚙️ ConfigMap Values</h2>
            <p>APP_ENV: <b>{}</b></p>
            <p>APP_VERSION: <b>{}</b></p>

            <h2>🔒 Secret Values</h2>
            <p>DB_PASSWORD: <b>{}</b></p>

            <h2>📄 Mounted Config File</h2>
            <pre style="background: white; padding: 10px;">{}</pre>
        </body>
    </html>
    """.format(
        os.environ.get("HOSTNAME", "unknown"),
        socket.gethostbyname(socket.gethostname()),
        visits,
        redis_status,
        app_env,
        app_version,
        db_password,
        config_file
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=False)