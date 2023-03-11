# Call http://localhost:8000/ for the main page
# Call http://localhost:8000/api/complete to complete a drawing

# Good edit prompt: "beautiful, stunning, award-winning, fantastic, realistic, professional"

from flask import Flask
from flask import send_from_directory, request

app = Flask(__name__)

@app.route("/<path:path>")
def hello_world(path):
    dir = path or "index.html"
    return send_from_directory("static", path)

@app.route("/api/complete", methods=['POST'])
def complete():
    return {"image": request.json['image']}

if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=8000)