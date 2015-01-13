/*
 * board.js - manage board
 */
var board = {
  init: function() {
    console.log("Initializing board");
    init_ws(WS_URL);
  }
};

// var box = $("#box");
//   $("[id^=box]").click(function() {
//       console.log("clicked box!");
//       console.log(this.id);
//       ws.send(this.id.slice(3));
//     });

//   function update_fill(data){
//     console.log("updating fill");
//     for (var i=0; i<10; i++)
//     {
//       fill = (data[i]) ? "green" : "white";
//       console.log(data[i]);
//       console.log(fill);
//       id = "#box" + i;
//       console.log(id);
//       $(id).css("background-color", fill);
//     }
//   }
