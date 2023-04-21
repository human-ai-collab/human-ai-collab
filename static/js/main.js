// Initialize variables
let tracer, drawingCanvas;
let mode = 2;
let weight = 10;
let slider;
// Sets the size of the canvas.
const IMAGE_WIDTH = 1280;
const IMAGE_HEIGHT = 720;

// // Placeholder image that you can load onto the canvas to test stuff.
// let placeholderDrawing;

// this is the "module" verson of the p5 setup function. Works the same way as setup(){}
setup = function setup() {
  const p5Renderer = createCanvas(IMAGE_WIDTH, IMAGE_HEIGHT);
  frameRate(60);
  drawingCanvas = p5Renderer.canvas;
  tracer = new Tracer(drawingCanvas, 2000);
  background(235)
  slider = createSlider(0, 255, 100);
  slider.position(10, 10);
  slider.style('width', '80px');
}

// this is the "module" verson of the p5 draw function. Works the same way as draw(){}
function draw() {
  // adjust brush weight
  weight = slider.value()/10
  // Move the tracer a little bit.
  tracer.draw();

  if(keyIsPressed && key == 'e'){
    mode = 1;
  } else if(keyIsPressed && key == 'd'){
    mode = 0; 
  }
  else if(keyIsPressed && key == 's'){
    mode = 2;
  }
}