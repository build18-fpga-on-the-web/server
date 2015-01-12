$(document).ready(function() {

      var ws;
      var box = $("#box");
      $("[id^=box]").click(function() {
          console.log("clicked box!");
          console.log(this.id);
          ws.send(this.id.slice(3));
        });

      function update_fill(data){
        console.log("updating fill");
        for (var i=0; i<10; i++)
        {
          fill = (data[i]) ? "green" : "white";
          console.log(data[i]);
          console.log(fill);
          id = "#box" + i;
          console.log(id);
          $(id).css("background-color", fill);
        }
      }

      function openWS(messageContainer) {
        ws = new WebSocket("ws://localhost:8081/chat");
        ws.onmessage = function(e) {
          console.log("new message");
          console.log(e);
          console.log(typeof(e.data));
          console.log(e.data);
          var data = JSON.parse(e.data);
          update_fill(data);
        };

        ws.onclose = function(e) {
          openWS(messageContainer);
        };
      }
      openWS();
    });
