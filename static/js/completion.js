// Get the next iteration of the image from the server. Returns a promise.
function getCompletion(drawingCanvas, completeCanvas) {
  return (
    sendImage(drawingCanvas)
    .then(resp => resp.json())
    .then(data => loadDataURL(data.image, completeCanvas))
  );
}

// Load image from a dataURI onto the specified canvas.
function loadDataURL(dataURL, canvas) {
  const myPromise = new Promise((resolve, reject) => {
    let context = canvas.getContext('2d');
    // load image from data url
    let imageObj = document.createElement("img")
    imageObj.onload = function() {
      context.drawImage(this, 0, 0);
      setTimeout(_ => resolve(), 1000)
      // resolve();
    };
    imageObj.src = dataURL;
  });
}

// Send encoded image to server using a fetch request
function sendImage(drawingCanvas) {
  return fetch("/api/complete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "image": canvasToBase64(drawingCanvas)
    })
  });
}

// Convert canvas pixels to a dataURI
function canvasToBase64(canvas) {
  let imageData = canvas.toDataURL('image/png'); // produces a base64 image string
  return imageData;
}