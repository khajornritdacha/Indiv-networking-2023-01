# slave
import socket
from overdrive import Overdrive

car = Overdrive("D5:C7:94:15:78:8D")

cur_ip = "kangbid.local"
cur_port = 7956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cur_ip, cur_port))
server.listen()
print(f"Listening on {cur_ip}:{cur_port}")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr[0]}:{addr[1]}")

while True :
    request = client_socket.recv(1024).decode("utf-8")
    if (request.lower() == "close") :
        client_socket.send("closed".encode("utf-8"))
        break

    print(f"Received: {request}")

    response = "accepted".encode("utf-8")
    car.changeSpeed(int(request), 1000)

client_socket.close()
server.close()
