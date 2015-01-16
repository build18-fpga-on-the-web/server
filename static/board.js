/*
 * board.js - manage board
 */
var data;

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
    for (var segment=0; segment<7; segment++)
    {
      if (!hex[i][segment])
      {
        $("#hex"+i+"-"+segment).addClass("on");
      }
      else
      {
        $("#hex"+i+"-"+segment).removeClass("on");
      }
    }
  }
  update_fill(inputs["key"], "#key", "grey");
  for (var i=0; i<inputs["sw"].length; i++){
    if (inputs["sw"][i]){
      if (!$("#inner_sw"+i).hasClass('on')){
       $("#inner_sw"+i).animate({ 'marginTop': "-=15" });
       $("#inner_sw"+i).toggleClass('on');
     }
    }
    else {
      if ($("#inner_sw"+i).hasClass('on')){
       $("#inner_sw"+i).animate({ 'marginTop': "+=15" });
       $("#inner_sw"+i).toggleClass('on');
     }

      }
  }
}

down = {};
function keyPress(e){
  switch (e.keyCode){
    case 49:
      if (down['49'] == null){
        down['49'] = true;
        $("#key3").css("background-color", "white");
        ws.send("key3");
      }
      break;
    case 50:
      if (down['50'] == null){
        ws.send("key2");
        down['50'] = true;
        $("#key2").css("background-color", "white");
      }
      break;
    case 51:
      if (down['51'] == null){
        ws.send("key1");
        down['51'] = true;
        $("#key1").css("background-color", "white");
      }
      break;
    case 52:
      if (down['52'] == null){
        ws.send("key0");
        down['52'] = true;
        $("#key0").css("background-color", "white");
      }
      break;
  }
}

function keyRelease(e){
  switch (e.keyCode){
    case 49:
      $("#key3").css("background-color", "grey");
      ws.send("key3");
      down['49'] = null;
      break;
    case 50:
      $("#key2").css("background-color", "grey");
      ws.send("key2");
      down['50'] = null;
      break;
    case 51:
      $("#key1").css("background-color", "grey");
      ws.send("key1");
      down['51'] = null;
      break;
    case 52:
      $("#key0").css("background-color", "grey");
      ws.send("key0");
      down['52'] = null;
      break;
  }
}

function buttonPress(e){
  switch (e.target.id){
    case "key0":
      if (down['49'] == null){
        $("#key0").css("background-color", "white");
        down['49'] = true;
        ws.send("key0");
      }
      break;
    case "key1":
      if (down['50'] == null){
        $("#key1").css("background-color", "white");
        ws.send("key1");
        down['50'] = true;
      }
      break;
    case "key2":
      if (down['51'] == null){
        $("#key2").css("background-color", "white");
        ws.send("key2");
        down['51'] = true;
      }
      break;
    case "key3":
      if (down['52'] == null){
        $("#key3").css("background-color", "white");
        ws.send("key3");
        down['52'] = true;
      }
      break;
  }
}

function buttonRelease(e){

  switch (e.target.id){
    case "key0":
      $("#key0").css("background-color", "grey");
      ws.send("key0");
      down['49'] = null;
      break;
    case "key1":
      $("#key1").css("background-color", "grey");
      ws.send("key1");
      down['50'] = null;
      break;
    case "key2":
      $("#key2").css("background-color", "grey");
      ws.send("key2");
      down['51'] = null;
      break;
    case "key3":
      $("#key3").css("background-color", "grey");
      ws.send("key3");
      down['52'] = null;
      break;
  }
}

var board = {
  init: function() {
    //console.log("Initializing board");
    this.init_ws(WS_URL);
    $(".switch").click(function() {
      console.log(this);
      var sw = $(this).children()[0];
      console.log(sw);
      $(sw).toggleClass('on');
      if ($(sw).hasClass('on')){
       $(sw).animate({ 'marginTop': "-=15" });
     }
     else{
      $(sw).animate({ 'marginTop': "+=15" });
     }
      ws.send(this.id);
    });
    $(document).keydown(keyPress);
    $(document).keyup(keyRelease);
    $(document).mousedown(buttonPress);
    $(document).mouseup(buttonRelease);

  },

  init_ws: function(url) {
    //console.log("Opening WebSocket");
    //console.log(url);
    ws = new WebSocket(url);
    ws.onopen = function(e) {
      $("#status").text("Status: Live");
      $("#status").css('color', 'LawnGreen');
    };
    ws.onmessage = function(e) {
      // console.log("new message");
      // console.log(e);
      // console.log(typeof(e.data));
      console.log(e.data);

      data = JSON.parse(e.data);
      $("#status").text("Status: Live("+data.clients+")");
      update_fills(data);
  };

  ws.onclose = function(e) {
    //console.log("WebSocket Closed");
    $("#status").text("Status: Dead");
    $("#status").css('color', 'red');
    this.init_ws(WS_URL);
  };
}
};


