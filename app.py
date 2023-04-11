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
import base64
from io import BytesIO
from PIL import Image, ImageShow
from waitress import serve

# Choose your port here
PORT = 8000
# Set to true if you want to enable AI features (faster)
ENABLE_AI = True
# PLACEHOLDER_FILE = "static/images/cat-better.png"
PLACEHOLDER_FILE = "static/images/danny.png"

# Only loads the AI library if it's allowed.
if ENABLE_AI:
  from ai import AI_complete


# PIL is an image format that our AI algorithm.
# dataURI is an image format that we send over http
# These two functions convert between the two.

# Converts PIL Image object to a dataURI PNG string.
def PIL_to_dataURI(img):
  buffered = BytesIO()
  ext = "PNG"
  img.save(buffered, format=ext)
  base64_utf8_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
  return f"data:image/{ext};base64,{base64_utf8_str}"

# Converts dataURI PNG string into a PIL Image object.
def dataURI_to_PIL(dataURI):
  assert len(dataURI.split(",")) == 2
  # image dataURI's follow the format data:image/png;base64,{A BUNCH OF CHARACTERS HERE}
  # We get the data portion of this string.
  dataPart = dataURI.split(",")[1]
  return Image.open(BytesIO(base64.decodebytes(bytes(dataPart, "utf-8"))))

# Locate the placeholder image that we use when AI is disabled.
placeholder_uri = PIL_to_dataURI(Image.open(PLACEHOLDER_FILE))

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
  input_PIL = dataURI_to_PIL(input_URI)

  # Check if AI is enabled (can be disabled for faster testing).
  if (not ENABLE_AI):
    # Send a placeholder to the user if AI is disabled.
    output = placeholder_uri
  else:
    # Use ai.py to compute an image if AI is enabled.
    output_PIL = AI_complete(input_PIL)
    output_URI = PIL_to_dataURI(output_PIL)
    output = PIL_to_dataURI(dataURI_to_PIL(output_URI))
  return {"image": output}

# This is basically equivalent to a "main" function in C++ or java.
if __name__ == "__main__":
  print(f"serving to http://localhost:{PORT}")
  print("READY!")
  # Start the server.
  serve(app, host="0.0.0.0", port=PORT)