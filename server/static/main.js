const socket = new WebSocket('ws://localhost:5000/ws');

const msg = text => document.getElementById('message').innerText = text;

socket.onopen = function(e) {
  msg("[open] Connection established");
//  alert("Sending to server");
//  socket.send("My name is John");
};

socket.onmessage = function(event) {

  // create a text element to draw in a CANVAS

  event.data.row
  event.data.column


  document.getElementById('screen').innerHTML = event.data;
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died', event.code, event.reason);
  }
};

socket.onerror = function(error) {
  alert(`[error]`);
};
