# to run, use "python3 ai.py"
# vvv PERFECT MODEL FOR OUR USE CASE!
# https://huggingface.co/spaces/huggingface-projects/diffuse-the-rest

import torch
import requests
from PIL import Image
from io import BytesIO
import os
import time

# Might have to use this command:
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
  """ Funtion that completes a drawing.
  :param object img input image
  :return completed image """
  # url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"
  # response = requests.get(url)
  # img = Image.open(BytesIO(response.content)).convert("RGB")

  original_height, original_width = img.size
  print(f"Original size: {(original_height, original_height)}")
  downscale_size = 512
  input_img = img.convert("RGB").resize((downscale_size, downscale_size))
  print(f"Processing size: {input_img.size}")
  print("Completing image...")
  images = pipe(
    image=input_img,
    prompt="Intricate realistic ink drawing, trending on ArtStation, full composition, photocopy",
    strength=0.5, # default 0.75
    guidance_scale=7.5, # default 7.5
    num_inference_steps=3, # default 50
    negative_prompt="beginner, colorful", # default nothing
    num_images_per_prompt=1 # default 1
  ).images

  # if it doesn’t exist we create one
  if not os.path.exists('output_dump'):
    os.makedirs('output_dump')
  images[0].save(f"output_dump/output-{int(time.time())}.png")

  output = images[0].resize((original_height, original_width))
  print(f"Output size: {output.size}")
  return output