# to run, use "python3 ai.py"
# vvv PERFECT MODEL FOR OUR USE CASE!
# https://huggingface.co/spaces/huggingface-projects/diffuse-the-rest

import torch
import requests
from PIL import Image
from io import BytesIO

# Might have to use this command:
# python3 -m pip install --upgrade diffusers accelerate transformers
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
if (torch.cuda.is_available()):
  device = "cuda:0"
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to(
    device
  )
else:
  device = "cpu"
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(
    device
  )

# let's download an initial image
url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

response = requests.get(url)
init_image = Image.open(BytesIO(response.content)).convert("RGB")
init_image.thumbnail((768, 768))

prompt = "A fantasy landscape, trending on artstation"

images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images

images[0].save("output/fantasy_landscape.png")