import socket

import time

HOST = "192.168.213.80"
PORT = 30002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(("set_standard_digital_out(0,True)" + "\n").encode('utf8'))
s.send(("set_standard_digital_out(1,True)" + "\n").encode('utf8'))
s.send(("movej([0.00268,-1.57192,-0.00124,-1.5717400000000001,-0.00136,0.0],a=1,v=1.05,t=0,r=0)" + "\n").encode('utf8'))

time.sleep(1)

s.close()
