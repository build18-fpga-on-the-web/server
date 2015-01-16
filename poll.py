import socket
import multiprocessing

HOST = "128.237.199.44"
PORT = 2540

class JTAGPoller(multiprocessing.Process):

    def __init__(self, taskQ, resultQ):
        multiprocessing.Process.__init__(self)
        self.taskQ = taskQ
        self.resultQ = resultQ
        self.DRlength = [0, 18, 9, 7, 7, 7, 7, 7, 7, 7, 7, 18, 4]
        self.firstRun = True
        self.inputs = [None]*13
        self.prevInputs = [None]*13

    def openSocket(self):
        self.size = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))

    def sendData(self, IR, data, length):
        # print("sendData", data)
        value = "".join(map(str, list(reversed(data)))) # convert int to a binary string
        # print(value)
        message = "send " + str(IR) + " " + str(value) + " " + str(length) + '\n'
        # newline is required to flush the buffer on the Tcl server
        self.conn.send(message.encode())

    def readData(self, IR, length):

        # self.conn.send("read " + str(IR) + " " + str(length) + '\n')
        # print(type(IR), type(length))
        message = "read " + str(IR) + " " + str(length) + '\n'
        # print("message", type(message))
        self.conn.send(message.encode())
        data = self.conn.recv(4096).decode()
        # print("readData", data)
        data = data.strip()
        data = list(map(int, data))
        return list(reversed(data))

    def closeSocket(self):
        self.conn.close()

    def run(self):

        self.openSocket() # open socket to Tcl server

        while True:
            # look for incoming tornado request
            if not self.taskQ.empty():
                task = self.taskQ.get()

                # parse SW and KEY data out of dict and send
                self.sendData(11, task["sw"], self.DRlength[11])
                self.sendData(12, task["key"], self.DRlength[12])

                # print("Sent to board: ", task)

            # poll board for inputs
            self.inputs = [self.readData(i, self.DRlength[i]) for i in range(1, 11)]
            inputD = {}
            inputD["ledr"] = self.inputs[0]
            inputD["ledg"] = self.inputs[1]
            inputD["hex"] = self.inputs[2:]
            self.inputs = inputD
            # check for differences and put an updated dict in the queue
            if (self.inputs != self.prevInputs):
                # print("SELF.INPUTS")
                # print(self.inputs)

                self.resultQ.put(self.inputs)
                self.prevInputs = self.inputs

