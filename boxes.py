from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, asynchronous
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode

import os.path

# Global variables shared between clients
clients = []
data = [0]*10;

class IndexHandler(RequestHandler):
    @asynchronous
    def get(request):
        request.render("index.html", data=data)

class WebSocketChatHandler(WebSocketHandler):
    def open(self, *args):
        print("open", "WebSocketChatHandler")
        clients.append(self)
        self.write_message(json_encode(data))

    def on_message(self, message):
        global data
        print(message)
        print(type(message))
        i = int(message)

        # Toggle data
        data[i] = 1 - data[i]
        # Send to all clients
        for client in clients:
            client.write_message(json_encode(data))

    def on_close(self):
        clients.remove(self)

def main():
    app = Application(
        [
            (r'/chat', WebSocketChatHandler),
            (r'/', IndexHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
    app.listen(8081)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
