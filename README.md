![Title screen.](docs/welcome.png)

# pAInt5

Your AI Drawing Buddy.

![Video demostratino, no audio.](docs/demo.gif)

## Running the Server

This webapp has a backend running on Python (Flask) with a StableDiffusion img2img pipeline. Here are the installation steps, assuming that you have cloned the project, cd's into it, and have pip3 installed.

1. Clone the repo to your machine.
2. `cd` into it.
3. Install all python dependencies: `pip3 install -r ./requirements.txt`
4. Run the server: Use the command `python3 app.py` to run the server. AI features can take up a lot of space and make the server take longer to start up and respond to queries. To disable them, use `python3 app.py no-ai` instead.
5. Now that your server is hosting locally, go to your web browser and visit `http://localhost:8000` on your computer to view the website. To try out the work-in-progress image-tracing features, visit `http://localhost:8000/ai-test.html`.

## Contributors

* Sam Hessian
* Daniel Dirksen
* Eric Chen
* Grace Hutapea
* Luke Wang
* Mina Jung