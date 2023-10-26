# slave1    ``
import socket
from overdrive import Overdrive

# Shock
car = Overdrive("CE:71:D1:FC:B5:4F")

cur_ip = "jopi.local"
cur_port = 7956

next_ip = "kangbid.local"
next_port = 7956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cur_ip, cur_port))
server.listen()
print(f"Listening on {cur_ip}:{cur_port}")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr[0]}:{addr[1]}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((next_ip, next_port))

while True :
    try:
        request = client_socket.recv(1024).decode("utf-8")
        if (request.lower() == "close") :
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        response = "accepted".encode("utf-8")
        car.changeSpeed(int(request[5:]), 1000)
        client.send(request.encode("utf-8"))
    except Exception as e:
        print(e)

client.close()
client_socket.close()
server.close()
