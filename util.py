# PIL is an image format that our AI algorithm.
# dataURI is an image format that we send over http
# These two functions convert between the two.

import base64
from PIL import Image
from io import BytesIO

# Converts PIL Image object to a dataURI PNG string.
def pillow_to_dataURI(img):
  buffered = BytesIO()
  ext = "PNG"
  img.save(buffered, format=ext)
  base64_utf8_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
  return f"data:image/{ext};base64,{base64_utf8_str}"

# Converts dataURI PNG string into a PIL Image object.
def dataURI_to_pillow(dataURI):
  assert len(dataURI.split(",")) == 2
  # image dataURI's follow the format data:image/png;base64,{A BUNCH OF CHARACTERS HERE}
  # We get the data portion of this string.
  dataPart = dataURI.split(",")[1]
  return Image.open(BytesIO(base64.decodebytes(bytes(dataPart, "utf-8"))))