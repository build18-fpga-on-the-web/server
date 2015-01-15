from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application, RequestHandler, asynchronous
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode
from fpga_process import FPGAProcess

import os.path
from multiprocessing import Queue

# Global variables shared between clients
clients = []
outputs = {}
inputs = {}
inputQ = None
num = {"ledr":18, "ledg":9, "hex":8, "segments":7, "sw":18, "key":4}

sev_seg = \
{0 : [ 1,  1,  1,  1,  1,  1,  0],
1 : [ 0, 1,  1,  0, 0, 0, 0],
2 : [ 1,  1,  0, 1,  1,  0, 1],
3 : [ 1,  1,  1,  1,  0, 0, 1],
4 : [ 0, 1,  1,  0, 0, 1,  1],
5 : [ 1,  0, 1,  1,  0, 1,  1],
6 : [ 1,  0, 1,  1,  1,  1,  1],
7 : [ 1,  1,  1,  0, 0, 1,  0],
8 : [ 1,  1,  1,  1,  1,  1,  1],
9 : [ 1,  1,  1,  1,  0, 1,  1],
'a' : [ 1,  1,  1,  0, 1,  1,  1],
'b' : [ 0, 0, 1,  1,  1,  1,  1],
'c' : [ 1,  0, 0, 1,  1,  1,  0],
'd' : [ 0, 1,  1,  1,  1,  0, 1],
'e' : [ 1,  0, 0, 1,  1,  1,  1],
'f' : [ 1,  0, 0, 0, 1,  1,  1]}

counter = 0
def num_to_segs(n):
    hexs = []
    for _ in range(8):
        hexs.append(sev_seg[n%10])
        n = n // 10
    return hexs

def init_outputs():
    outputs["ledr"] = [1]*18
    outputs["ledg"] = [1]*9
    outputs["hex"] = num_to_segs(counter)

def init_inputs():
    inputs["sw"] = [0]*18
    inputs["key"] = [0]*4

class IndexHandler(RequestHandler):
    @asynchronous
    def get(request):
        data = {"inputs":inputs, "outputs":outputs, "clients":len(clients)}
        request.render("index.html", data=data, num=num)

def send_data():
    data = {"inputs":inputs, "outputs":outputs, "clients":len(clients)}
    for client in clients:
        client.write_message(json_encode(data))

class WebSocketChatHandler(WebSocketHandler):
    def open(self, *args):
        print("open", "WebSocketChatHandler")
        clients.append(self)
        send_data()

    def on_message(self, message):
        group = None
        if message.startswith("sw"):
            group = "sw"
        if message.startswith("key"):
            group = "key"
        if group:
            try:
                i = int(message[len(group):])
            except ValueError:
                print("int failed on", message)
            inputs[group][i] = 1 - inputs[group][i]
        inputQ.put(inputs)
        send_data()

    def on_close(self):
        clients.remove(self)
        send_data()

    def check_origin(self, origin):
        return True

def main():
    global inputQ
    global outputs
    inputQ = Queue()
    outputQ = Queue()

    fp = FPGAProcess(inputQ, outputQ)
    fp.daemon = True
    fp.start()

    init_outputs()
    init_inputs()
    app = Application(
        [
            (r'/chat', WebSocketChatHandler),
            (r'/', IndexHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        )
    app.listen(8081)

    print("Listening on port 8081")
    def periodic_callback():
        global outputs
        if not outputQ.empty():
            outputs = outputQ.get()
            print("From output queue")
            print(outputs)
            send_data()

    mainloop = IOLoop.instance()
    scheduler = PeriodicCallback(periodic_callback, 10, io_loop = mainloop)
    scheduler.start()
    mainloop.start()

if __name__ == "__main__":
    main()
