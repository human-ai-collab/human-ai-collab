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
from PIL import Image
from waitress import serve
import sys
from util import pillow_to_dataURI, dataURI_to_pillow

# Choose your port here
PORT = 8000

# Run "python3 app.py" if you want to enable AI features (slower)
# Run "python3 app.py no-ai" if you want to enable AI features (faster)
enableAI = False if "no-ai" in sys.argv else True
# PLACEHOLDER_FILE = "static/images/cat-better.png"

# Only loads the AI library if it's allowed.
if enableAI:
  from ai import AI_complete
else:
  PLACEHOLDER_FILE = "static/images/cat-better.png"
  # Locate the placeholder image that we use when AI is disabled.
  placeholder_uri = pillow_to_dataURI(Image.open(PLACEHOLDER_FILE))

# Initialize a new python flask server.
app = Flask(__name__)

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

  # Check if AI is enabled (can be disabled for faster testing).
  if (not enableAI):
    # Send a placeholder to the user if AI is disabled.
    output = placeholder_uri
  else:
    # Use ai.py to compute an image if AI is enabled.
    output_PIL = AI_complete(input_PIL)
    output_URI = pillow_to_dataURI(output_PIL)
    output = pillow_to_dataURI(dataURI_to_pillow(output_URI))
  return {"image": output}

# This is basically equivalent to a "main" function in C++ or java.
if __name__ == "__main__":
  print(f"serving to http://localhost:{PORT}")
  print("READY!")
  # Start the server.
  serve(app, host="0.0.0.0", port=PORT)