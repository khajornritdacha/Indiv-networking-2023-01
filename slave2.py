# slave2
import socket
from overdrive import Overdrive
from carEnum import CarOperation

# Skull
car = Overdrive("D5:C7:94:15:78:8D")

PI_NAME = "KANGBID"
CAR_NAME = "SKULL"

cur_ip = "kangbid.local"
cur_port = 7956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cur_ip, cur_port))
server.listen()
print(f"Listening on {cur_ip}:{cur_port}")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr[0]}:{addr[1]}")

while True :
    try:
        request = client_socket.recv(1024).decode("utf-8")
        op, speed = request.split()
        op = op.lower()
        speed = int(speed)

        if op == CarOperation.CLOSE.value :
            client_socket.send(CarOperation.CLOSE.value.encode("utf-8"))
            break
                
        if op == CarOperation.ACCEL.value:
            car.changeSpeed(int(request[5:]), 1000)
            response = CarOperation.OK.encode("utf-8")

        elif op == CarOperation.DECEL.value:            
            car.changeSpeed(speed, 1000)
            response = CarOperation.OK.encode("utf-8")

    except Exception as e:
        print(e)
        
client_socket.close()
server.close()
