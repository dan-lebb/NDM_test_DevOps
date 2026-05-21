from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():

    result = []

    result.append(f"REMOTE_ADDR: {request.remote_addr}")
    result.append("")

    result.append("HEADERS:")

    for k, v in request.headers.items():
        result.append(f"{k}: {v}")

    return "\n".join(result), 200, {
        "Content-Type": "text/plain"
    }

app.run(host="0.0.0.0", port=5000)
