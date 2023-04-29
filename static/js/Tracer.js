class Tracer {
  // Define static variables
  static hasRunSetup = false;

  static drawingCanvas; // The canvas that the tracer will draw on.
  static completeCanvas; // The canvas that the tracer will use as reference;
  static drawingCTX; // The rendering context for drawingCanvas.
  static completeCTX; // The rendering context for completeCanvas.
  static imageSize;
  static drawingData;
  static completeData;

  /**
   * @param {Canvas} _drawingCanvas the canvas that the tracer will draw on.
   * @param {Number} speed Number of drawing steps taken each frame.
   */
  constructor(_drawingCanvas, speed = 1) {
    this.paused = true;
    this.stepsPerFrame = speed;
    if (!Tracer.hasRunSetup) {
      Tracer.setup(_drawingCanvas);
      Tracer.hasRunSetup = true;
    }
  
    this.pos = createVector(0,0);
    this.oldPos = createVector(0,0);
    this.newPos = createVector(0,0);
    this.bestNewPos = createVector(0,0);
    this.bestNewAngle = null;
    this.startingRot = null;
    this.strokeValue = null;
    this.smoothStrokeWeight = null;
    this.mustResetPos = true; // flag that indicates that the brush pos needs to be reset
    this.resetPos();
  }

  startTracing() {
    this.paused = false;
  }

  forgetCompletion() {
    Tracer.completeCTX.drawImage(Tracer.drawingCanvas, 0, 0);
  }

  stopTracing() {
    this.paused = true;
    Tracer.completeCanvas.style.display = "inline-block"
  }

  setSpeed(speed) {
    this.stepsPerFrame = speed;
  }

  /* 
   * This setup function only needs to run once for all tracers.
   * @param _drawingCanvas the canvas that the tracer will draw on.
   */
  static setup(_drawingCanvas) {
    // Drawing Canvas
    pixelDensity(1)
    // Initialize Canvases
    Tracer.drawingCanvas = _drawingCanvas;
    Tracer.imageWidth = Tracer.drawingCanvas.width;
    Tracer.imageHeight = Tracer.drawingCanvas.height;
    const parentEl = document.querySelector("main");
    
    Tracer.drawingCTX = Tracer.drawingCanvas.getContext('2d', { willReadFrequently: true });
    Tracer.drawingCTX.willReadFrequently = true;
    
    // Complete Canvas
    Tracer.completeCanvas = document.createElement("canvas");
    parentEl.appendChild(Tracer.completeCanvas);
    this.completeCanvas.style.display="none";
    Tracer.completeCanvas.width = Tracer.imageWidth;
    Tracer.completeCanvas.height = Tracer.imageHeight;
    Tracer.completeCTX = Tracer.completeCanvas.getContext('2d', { willReadFrequently: true });
    Tracer.completeCTX.willReadFrequently = true;
    Tracer.completeCTX.fillStyle = "#FFF";
    Tracer.completeCTX.fillRect(0, 0, Tracer.imageWidth, Tracer.imageHeight);
  }
  draw() {
    if (!this.paused) {
      if (this.mustResetPos) {
        this.findGoodStartingPlace();
        this.mustResetPos = false;
      } else {
        // Take a few steps each frame.
        for (let j = 0; j < this.stepsPerFrame; j ++) {
          this.stepForward();
          if (this.mustResetPos) break;
        }
      }
    }
    Tracer.drawingData = Tracer.drawingCTX.getImageData(0, 0, Tracer.drawingCanvas.width, Tracer.drawingCanvas.height);
    Tracer.completeData = Tracer.completeCTX.getImageData(0, 0, Tracer.completeCanvas.width, Tracer.completeCanvas.height);
  }
  
  /**
   * Keeps picking random positions on the canvas until we find a good starting place.
   */
  findGoodStartingPlace() {
    for (let i = 0; i < 2000; i ++) {
      this.resetPos();
      this.smoothStrokeWeight = 2;
      if (Math.abs(Tracer.differenceAt(this.pos)) > 50) {
        const preciseValue = Tracer.valueAt(this.pos, Tracer.completeData);
        const noise = 4 * (Math.random() - 0.5);
        this.strokeValue = Math.min(Math.max(0, preciseValue + noise), 255);
        return;
      }
    }
    // Stop tracing if too many attempts were made.
    console.log("stop")
    this.stopTracing();
  }
  
  
  /**
   * Steps the AI brush forward, choosing the optimal next step.
   */
  stepForward() {
    this.bestNewPos.set(this.pos);
    let greatestErrorReduction = 0;
  
    
    // Use this to configure the search area and spread.
    // angleDeviation: how far angle can deviate from previous angle, in radians
    // samples: Number of samples when deciding a turn. Should be at least 3.
    const angleDeviation = this.startingRot ? 0.5 : Math.PI/2;
    const samples = this.startingRot ? 15 : 33;
    const STEP_SIZE = 1 + 1.4 * this.smoothStrokeWeight;
    const leapLength = Math.random() + STEP_SIZE + (this.startingRot ? 0 : 0);
    if (!this.startingRot) this.startingRot = 2 * Math.PI * Math.random();
  
    // Calculate spread based on the above factors.
    const lowerBound = this.startingRot - angleDeviation;
    const upperBound = this.startingRot + angleDeviation;
    const increment = 2 * angleDeviation / (samples - 1);
  
    let maxWeight = 10;
    let numAnglesImproved = 0;
    for (let newAngle = lowerBound; newAngle <= upperBound; newAngle += increment) {
  
      // Calculate where this new direction would land us if we took it, with some randomness.
      this.newPos.set(leapLength, 0);
      this.newPos.rotate(newAngle);
      this.newPos.add(this.pos);
  
      // Measure how well the stroke color matches this spot.
      const errorWith = Math.abs(Tracer.valueAt(this.newPos, Tracer.completeData) - this.strokeValue);
      const errorWithout = Math.abs(Tracer.differenceAt(this.newPos));
      const turnAmount = Math.abs(newAngle - this.startingRot); // Break ties by prefering the smallest turn.
  
      const newErrorReduction = errorWithout - errorWith - 0.1 * turnAmount; // Positive values good.
  
      // const TYPICAL_WEIGHT = 1;
      if (newErrorReduction > 5) numAnglesImproved ++;
      
      let updateBest = false;
      if (Tracer.inBounds(this.newPos)) {
        if (newErrorReduction > greatestErrorReduction) {
          updateBest = true;
        }
      }
      if (updateBest) {
        this.bestNewPos.set(this.newPos);
        this.bestNewAngle = this.newAngle;
        greatestErrorReduction = newErrorReduction;
      }
    }
  
    if (greatestErrorReduction > 5) {
      const newStrokeWeight = (leapLength) * (numAnglesImproved / samples);
      if (newStrokeWeight > this.smoothStrokeWeight) {
        this.smoothStrokeWeight += 1;
      } else {
        this.smoothStrokeWeight -= 1;
        this.smoothStrokeWeight = Math.max(2, this.smoothStrokeWeight);
      }
      strokeWeight(this.smoothStrokeWeight);
      const opacity = 200 // out of 255. The greater, the more opaque
      const value = this.strokeValue
      if (value < 0 || value > 255) console.log(value)
      stroke(value, opacity);
      this.oldPos.set(this.pos);
      this.pos.lerp(this.bestNewPos, 0.2);
      line(this.oldPos.x, this.oldPos.y, this.pos.x, this.pos.y);
    } else {
      if (Math.random() < 0.1) {
        this.mustResetPos = true;
      } else {
        this.startingRot = null;
      }
    }
  }
  
  /**
   * Resets the AI brush to a random position on the screen, pointing it in a random direction.
   */
  resetPos() {
    this.pos.x = Math.floor(Math.random() * Tracer.imageWidth);
    this.pos.y = Math.floor(Math.random() * Tracer.imageHeight);
    this.startingRot = null;
  }

  static getRedIndexForCoord = (x, y, width) => {
    const red = Math.floor(y) * (width * 4) + Math.floor(x) * 4;
    return red;
  };
  
  /**
   * Calculate the the value of a canvas context at a certain position.
   * @param {P5 Vector} pos - The position to search at
   * @param {Canvas Context} ctx - The context of the canvas to search.
   * @return {number} The difference
   */
  static valueAt(pos, imageData) {
    const redIndex = Tracer.getRedIndexForCoord(pos.x, pos.y, imageData.width);
    const value = (imageData.data[redIndex] + imageData.data[redIndex+1] + imageData.data[redIndex+2]) / 3;
    const noise = Math.random();
    return value + noise;
  }
  
  /**
   * Calculate the difference between what is and what should be. Positive if it should be lighter, negative if it should be darker.
   * @param {P5 Vector} pos - The position to search at
   * @return {number} The difference
   */
  static differenceAt(pos) {
    return Tracer.valueAt(pos, Tracer.completeData) - Tracer.valueAt(pos, Tracer.drawingData);
  }
  
  static inBounds(pos) {
    return pos.x >= 0 && pos.y >= 0 && pos.x < Tracer.imageWidth && pos.y < Tracer.imageHeight;
  }
}