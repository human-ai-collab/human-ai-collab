"""
This file is for the arguments we will give the AI algorithm for how to process the image.
These are the arguments for the pipe() function in ai.py which runs the stable-diffusion algorithm.
Feel free to try different things with this and keep track of your findings.
"""

# Before processing the image, we scale it down to make it process faster.
# downscale_size specifies the largest dimension (height or width) we want the downscaled version
# to have.
downscale_size = 1280

arguments = {
  # Change this to change the text prompt for how to edit the image.
  # "prompt": "Realistic graphite sketch by Rembrandt, museum, full composition, photocopy",
  "prompt": "Realistic ink drawing, trending on ArtStation, full composition, photocopy",
  # "prompt": "Realistic graphic sketch, trending on ArtStation, full composition, photocopy",
  # How strongly the image is affected.
  # Default: 0.75
  "strength": 0.46,

  # How strongly the image should match the prompt.
  # Default: 7.5
  "guidance_scale": 7.5,

  # How many steps the AI takse to make the image looks better. More is faster but a lot slower.
  # I'd keep this low while testing.
  # Default: 50
  "num_inference_steps": 15,

  # Tells AI what NOT to do.
  # Default: ""
  "negative_prompt": "beginner, colorful",

  # Keep this at 1.
  # Default: 1
  "num_images_per_prompt": 1
}