from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    try:
        res = requests.get("http://service-a:5001/")
        return f"Service B calling A: {res.text}"
    except Exception as e:
        return f"Service B: Could not reach Service A. Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
