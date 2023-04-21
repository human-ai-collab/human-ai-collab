# MAIN BACKEND FILE

"""
Viewing:
  Visit http://localhost:8000/index.html for the main page.
  Visit http://localhost:8000/send-image.html to see the WIP image-tracing algorithm.
How the REST API works: Send request to http://localhost:8000/api/complete 
  with {"image": "data:PNG;base64,iVBORw0KGgo..."} to request a drawing completion
"""

# Import requried libraries
from flask import Flask
from flask import send_from_directory, request
from waitress import serve
import sys
from util import pillow_to_dataURI, dataURI_to_pillow
import ai
import webbrowser

# Choose your port here
PORT = 8000

# Run "python3 app.py" if you want to enable AI features (slower)
# Run "python3 app.py no-ai" if you want to enable AI features (faster)
enable_ai = False if "no-ai" in sys.argv else True
ai.init(enable_ai, placeholder_image_path="static/images/cat-better.png")

# Initialize a new python flask server.
app = Flask(__name__)

def open_webbrowser():
  webbrowser.open_new("http://localhost:8000/welcome.html")

# Serve the static site
@app.route("/")
@app.route("/<path:path>")
def static_site(path=None):
  if (path == None):
    # If url has no path, send index.html.
    return send_from_directory("static", "index.html")
  else:
    # Otherwise, give user the whatever file they request.
    return send_from_directory("static", path)

# Send it an image and it will complete it with AI and send it back.
@app.route("/api/complete", methods=['POST'])
def ai_complete():
  # Get request body, which is formatted as {"image": "data..."}
  body = request.json
  # dataURI for input image
  input_URI = body['image']
  # convert to Pillow image object
  input_PIL = dataURI_to_pillow(input_URI)

  # Use ai.py to compute an image if AI is enabled.
  output_PIL = ai.complete_image(input_PIL)
  output_URI = pillow_to_dataURI(output_PIL)
  output = pillow_to_dataURI(dataURI_to_pillow(output_URI))
  return {"image": output}

# This is basically equivalent to a "main" function in C++ or java.
if __name__ == "__main__":
  print(f"serving to http://localhost:{PORT}")
  print("READY!")
  # Start the server.
  open_webbrowser()
  serve(app, host="0.0.0.0", port=PORT, threads=10)
