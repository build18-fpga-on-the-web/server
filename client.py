
from websocket import create_connection
import time
ws = create_connection("ws://localhost:8081/chat")
print("Sending 'Hello, World'...")
sw = 0
while True:
    message = "sw%d"%sw
    print("Sending", message)
    ws.send(message)
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    sw = (sw + 1)%18
    time.sleep(0.1)
ws.close()
