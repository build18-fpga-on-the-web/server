import socket
import time
from fpga_process import FPGAProcess

host = 'localhost'
port = 2540
size = 1024

def Open(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(( host,port))
	return s

def SendData(conn,IR,data,length):
    value = bin(data).split('0b')[1].zfill(length) #Convert from int to binary string
    conn.send("send " + str(IR) + " " + str(value) + " " + str(length) + '\n') #Newline is required to flush the buffer on the Tcl server

def ReadData(conn,IR,length):
	conn.send("read " + bin(IR) + " " + bin(length) + '\n')
	print "test\n"
	print conn.recv(4096) + '\n'



conn = Open(host, port)
print "Connected"

while True:
    ReadData(conn,1,18)
    time.sleep(1)

conn.close()



