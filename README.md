# A Human-AI Collaboration Pad.

## Running the Server

This webapp has a backend running on Python (Flask) with a StableDiffusion img2img pipeline. Here are the installation steps, assuming that you have cloned the project, cd's into it, and have pip3 installed.

1. Clone the repo to your machine.
2. `cd` into it.
3. Install all python dependencies: `pip3 install -r ./requirements.txt`
4. Run the server: Use the command `python3 app.py` to run the server. AI features can take up a lot of space and make the server take longer to start up and respond to queries. To disable them, use `python3 app.py no-ai` instead.
5. In your web browser, visit `http://localhost:8000` to view the website. To try out the work-in-progress image-tracing features, visit `http://localhost:8000` on your computer.

## Try it! (COMING SOON)

## Contributors