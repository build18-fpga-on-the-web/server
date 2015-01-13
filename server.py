from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, asynchronous
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode

import os.path

# Global variables shared between clients
clients = []
outputs = {}
inputs = {}
num = {"ledr":18, "ledg":9, "hex":8, "segments":7, "sw":18, "key":4}

def init_outputs():
    outputs["ledr"] = [0]*18
    outputs["ledg"] = [0]*9
    outputs["hex"] = [[0]*7 for _ in range(8)]

def init_inputs():
    inputs["sw"] = [0]*18
    inputs["key"] = [0]*4

class IndexHandler(RequestHandler):
    @asynchronous
    def get(request):
        data = {"inputs":inputs, "outputs":outputs}
        request.render("index.html", data=data, num=num)

class WebSocketChatHandler(WebSocketHandler):
    def open(self, *args):
        print("open", "WebSocketChatHandler")
        clients.append(self)
        self.write_message(json_encode(data))

    def on_message(self, message):
        print("Message from client")
        print(message)
        data = {"inputs":inputs, "outputs":outputs}
        for client in clients:
            client.write_message(json_encode(data))

    def on_close(self):
        clients.remove(self)

    def check_origin(self, origin):
        return True

def main():
    init_outputs()
    init_inputs()
    app = Application(
        [
            (r'/chat', WebSocketChatHandler),
            (r'/', IndexHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
    app.listen(8081)
    print("Listening on port 8081")
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
