from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🚀 Hello from Jijash !</h1>
            <p>This app is running inside a <b>Pod</b> on Minikube!</p>
            <p>Pod Name: <b>{}</b></p>
            <p>Pod IP: <b>{}</b></p>
        </body>
    </html>
    """.format(
        os.environ.get("HOSTNAME", "unknown"),
        socket.gethostbyname(socket.gethostname())
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "pod": os.environ.get("HOSTNAME", "unknown")
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=False)