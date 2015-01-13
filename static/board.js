/*
 * board.js - manage board
 */

function update_fill(data, class_name, color) {
  for (var i=0; i<data.length; i++)
  {
    fill = (data[i]) ? color : "white";
    id = class_name + i;
    $(id).css("background-color", fill);
  }
}

function update_fills(data) {
  var outputs = data["outputs"];
  var inputs = data["inputs"];
  update_fill(outputs["ledr"], "#ledr", "red");
  update_fill(outputs["ledg"], "#ledg", "green");
  var hex = outputs["hex"];
  for (var i=0; i<hex.length; i++)
  {
    update_fill(hex[i], "#hex"+i+"-", "red");
  }
  // update_fill(inputs["sw"], "#sw", "grey");
  update_fill(inputs["key"], "#key", "grey");
}


var board = {
  init: function() {
    console.log("Initializing board");
    this.init_ws(WS_URL);
    $(".switch").click(function() {
      $(this).children().toggleClass('on');
      ws.send(this.id);
    });
    $(".key").click(function() {
      ws.send(this.id);
    });
  },

  init_ws: function(url) {
    console.log("Opening WebSocket");
    console.log(url);
    ws = new WebSocket(url);
    ws.onopen = function(e) {
      $("#status").text("Status: Live");
      $("#status").css('color', 'LawnGreen');
    };
    ws.onmessage = function(e) {
      console.log("new message");
      console.log(e);
      console.log(typeof(e.data));
      console.log(e.data);
      var data = JSON.parse(e.data);
      update_fills(data);
  };

  ws.onclose = function(e) {
    console.log("WebSocket Closed");
    $("#status").text("Status: Dead");
    $("#status").css('color', 'red');
    init_ws(url);
  };
}
};
