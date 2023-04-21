"""
This file contains just the AI script 
Here is another model we could consider using use:
  https://huggingface.co/spaces/huggingface-projects/diffuse-the-rest
Good edit prompt: "beautiful, stunning, award-winning, fantastic, realistic, professional"
"""

# Import all libraries.
import torch
import os
import time
import importlib
import prompt
from PIL import Image

_pipe = None
_placeholder_image_path = None

def init(enable_ai = True, placeholder_image_path = None):
  # Tell python that these are global, not local variables.
  global _pipe, _placeholder_image_path

  _placeholder_image_path = placeholder_image_path
  if (enable_ai and _pipe is None):
    # If this line doesn't work, you might have to use this command:
    # python3 -m pip install --upgrade diffusers accelerate transformers
    from diffusers import StableDiffusionImg2ImgPipeline
    # Load the pipeline.
    if (torch.cuda.is_available()):
      device = "cuda:0"
      torch_dtype=torch.float16
      _pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch_dtype).to(device)
    else:
      device = "cpu"
      _pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(device)
    # Remove safety checks.
    _pipe.safety_checker = lambda images, clip_input: (images, False)

def _placeholder(img):

  # Tell python that these are global, not local variables.
  global _pipe, _placeholder_image_path
  
  # Locate the placeholder image that we use when AI is disabled.
  output = Image.open(_placeholder_image_path).copy()
  output.resize(img.size)
  return output

def complete_image(img):
  """ Funtion that completes a drawing using HuggingFace StableDiffusion.
  :param object img input image
  :return completed image """

  # Tell python that these are global, not local variables.
  global _pipe, _placeholder_image_path

  if (_pipe is None):
    return _placeholder(img)

  # Get an up-to-date prompt, in case the file changed.
  importlib.reload(prompt)

  # Save the origional image size so that we can downscale it, then scale it back up to the origional.
  original_height, original_width = img.size
  aspect_ratio = original_width / original_height
  # The size that we downscale the image to.

  # Scale the image so that neither dimension excedes downscale_size.
  if (aspect_ratio > 1):
    downscale_width = prompt.downscale_size
    downscale_height = int(prompt.downscale_size / aspect_ratio)
  else:
    downscale_width = int(prompt.downscale_size * aspect_ratio)
    downscale_height = prompt.downscale_size

  # Remove the image "alpha" channel and size it down.
  input_img = img.convert("RGB").resize((downscale_height, downscale_width))
  print("Completing image...")

  # Add the input image as one of the arguments.
  prompt.arguments["image"] = input_img

  # Run the model on the downscaled image.
  images = _pipe(**prompt.arguments).images

  # Dump the output image into "output_dump" folder for testing.
  # If it doesn’t exist we create one.
  if not os.path.exists('output_dump'):
    os.makedirs('output_dump')
  # Save the image to file with a timestamp.
  images[0].save(f"output_dump/output-{int(time.time())}.png")

  # Scale the image back to it's origional size, so that it fits perfectly onto the p5 canvas.
  output = images[0].resize((original_height, original_width))
  return output