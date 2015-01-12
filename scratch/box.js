$(document).ready(function() {
        $("#box").click(function() {
          console.log("clicked box!");
        });
      var ws;


      function openWS(messageContainer) {
        ws = new WebSocket("ws://localhost:8080/chat");
        ws.onmessage = function(e) {
          console.log("new message");
        };

        ws.onclose = function(e) {
          openWS(messageContainer);
        };
      }

      openWS();

    }
