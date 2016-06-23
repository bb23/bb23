import socket
from time import sleep

TCP_IP = '127.0.0.1'
TCP_PORT = 9101
BUFFER_SIZE = 30

def send_command(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(command + "\n")
    data = s.recv(BUFFER_SIZE)
    s.close()

    print "received data:", data


send_command("forward")
sleep(3)
send_command("turn_right")
sleep(3)
send_command("turn_left")
sleep(3)
send_command("stop")



