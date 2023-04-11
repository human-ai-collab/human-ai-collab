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
import json
import importlib
import prompt

# If this line doesn't work, you might have to use this command:
# python3 -m pip install --upgrade diffusers accelerate transformers
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
if (torch.cuda.is_available()):
  device = "cuda:0"
  torch_dtype=torch.float16
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch_dtype).to(device)
else:
  device = "cpu"
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(device)
pipe.safety_checker = lambda images, clip_input: (images, False)

def AI_complete(img):
  """ Funtion that completes a drawing using HuggingFace StableDiffusion.
  :param object img input image
  :return completed image """

  # Save the origional image size so that we can downscale it, then scale it back up to the origional.
  original_height, original_width = img.size
  # The size that we downscale the image to.
  downscale_size = 512
  # Remove the image "alpha" channel and size it down.
  input_img = img.convert("RGB").resize((downscale_size, downscale_size))
  print("Completing image...")

  # Get an up-to-date prompt, in case the file changed.
  importlib.reload(prompt)
  # Add the input image as one of the arguments.
  prompt.arguments["image"] = input_img

  # Run the model on the downscaled image.
  images = pipe(**prompt.arguments).images

  # Dump the output image into "output_dump" folder for testing.
  # If it doesn’t exist we create one.
  if not os.path.exists('output_dump'):
    os.makedirs('output_dump')
  # Save the image to file with a timestamp.
  images[0].save(f"output_dump/output-{int(time.time())}.png")

  # Scale the image back to it's origional size, so that it fits perfectly onto the p5 canvas.
  output = images[0].resize((original_height, original_width))
  return output