# Call http://localhost:8000/ for the main page
# Call http://localhost:8000/api/complete to complete a drawing

# Good edit prompt: "beautiful, stunning, award-winning, fantastic, realistic, professional"

from flask import Flask
from flask import send_from_directory, request
import base64
from io import BytesIO
from PIL import Image, ImageShow

def image_to_dataURI(img):
  buffered = BytesIO()
  ext = "PNG"
  img.save(buffered, format=ext)
  base64_utf8_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
  return f"data:image/{ext};base64,{base64_utf8_str}"

placeholder_img = Image.open("static/images/cat-better.png")
placeholder_uri = image_to_dataURI(placeholder_img)

app = Flask(__name__)

@app.route("/<path:path>")
def hello_world(path):
    dir = path or "index.html"
    return send_from_directory("static", path)

@app.route("/api/complete", methods=['POST'])
def complete():
  body = request.json
  input = body['image']
  output = placeholder_uri
  return {"image": output}

if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=8000)