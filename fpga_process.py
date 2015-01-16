import time
import multiprocessing

sev_seg = \
{0 : [ 1, 1, 1, 1, 1, 1, 0],
1 : [ 0, 1, 1, 0, 0, 0, 0],
2 : [ 1, 1, 0, 1, 1, 0, 1],
3 : [ 1, 1, 1, 1, 0, 0, 1],
4 : [ 0, 1, 1, 0, 0, 1, 1],
5 : [ 1, 0, 1, 1, 0, 1, 1],
6 : [ 1, 0, 1, 1, 1, 1, 1],
7 : [ 1, 1, 1, 0, 0, 1, 0],
8 : [ 1, 1, 1, 1, 1, 1, 1],
9 : [ 1, 1, 1, 1, 0, 1, 1],
'a' : [ 1, 1, 1, 0, 1, 1, 1],
'b' : [ 0, 0, 1, 1, 1, 1, 1],
'c' : [ 1, 0, 0, 1, 1, 1, 0],
'd' : [ 0, 1, 1, 1, 1, 0, 1],
'e' : [ 1, 0, 0, 1, 1, 1, 1],
'f' : [ 1, 0, 0, 0, 1, 1, 1],
'u' : [ 0, 0, 1, 1, 1, 0, 0],
'L' : [ 0, 1, 1, 0, 0, 0, 0],
'd' : [ 0, 1, 1, 1, 1, 0, 1],
'i' : [ 0, 0, 1, 0, 0, 0, 0],
' ' : [0]*7}

def flip(n):
    return 1 - n

def flip_hex(hex):
    return [list(map(flip, seg)) for seg in hex]

def num_to_segs(n):
    hexs = []
    for _ in range(8):
        hexs.append(list(map(flip, sev_seg[n%10])))
        n = n // 10
    return hexs

def sw_to_hex(sw):
    total = 0
    for i in range(18):
        total += sw[i]*(2**i)
    return total

class FPGAProcess(multiprocessing.Process):

    def __init__(self, inputQ, outputQ):
        multiprocessing.Process.__init__(self)
        self.inputQ = inputQ
        self.outputQ = outputQ

    def get_outputs(self, inputs):
        outputs = {}
        switches = inputs.get("sw", [0]*18)
        outputs["ledr"] = switches
        outputs["ledg"] = inputs.get("key", [0]*4)*2 + [1]
        outputs["hex"] = num_to_segs(sw_to_hex(switches))
        return outputs

    def run(self):
        prev_outputs = None
        inputs = {}
        while True:
            if not self.inputQ.empty():
                print("From inputQ")
                inputs = self.inputQ.get()
                print(inputs)
            outputs = self.get_outputs(inputs)
            if outputs != prev_outputs:
                self.outputQ.put(outputs)
                prev_outputs = outputs
            time.sleep(0.01)
