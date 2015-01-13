function openWS(messageContainer) {
    ws = new WebSocket(ws_url);
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
