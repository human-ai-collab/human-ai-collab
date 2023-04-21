// Code to load an example image when button is pressed.
function loadExample() {
  let placeholder = new Image();
  placeholder.onload = function() {
    const ctx = drawingCanvas.getContext('2d');
    ctx.drawImage(placeholder, 0, 0);
  }
  placeholder.src = 'images/cat-unfinished.png';
}

let timer = null
// Get an image completion from the backend. Taces for a minute, then rinse and repeat.
function complete() {
  getCompletion(drawingCanvas, Tracer.completeCanvas).then(() => {
    tracer.startTracing()
    // Trace for a minute, then get another completion.
    timer = setTimeout(() => {
      tracer.stopTracing();
      complete();
    }, 30 * 1000);
  });
}

function mouseDragged() {
  if(mode == 0){
    strokeWeight(weight);
    stroke(0);
    line(mouseX, mouseY, pmouseX, pmouseY);
  }
  else if( mode == 1){
    strokeWeight(weight);
    stroke(200);
    line(mouseX, mouseY, pmouseX, pmouseY);
  }
};

function clearScreen() {
  bgColor = color(random(360), random(100), random(100));
  background(235);
  text('Hold the e key to erase', 20,20);
}

function toggleDraw() {
  mode = 0;
}

function toggleErase() {
  mode = 1;
}

const timelapseCheckbox = document.getElementById("timelapse");
function toggleTimelapse() {
  tracer.setSpeed(timelapseCheckbox.checked ? 20 : 1);
}