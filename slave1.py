# slave1    ``
import socket
from overdrive import Overdrive
from carEnum import CarOperation
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

next_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
next_client.connect((next_ip, next_port))

while True :
    try:
        request = client_socket.recv(1024).decode("utf-8")
        if request.lower() == CarOperation.CLOSE.value :
            client_socket.send(CarOperation.CLOSE.value.encode("utf-8"))
            break
        
        op, speed = request.split()
        op = op.lower()
        speed = int(speed)

        if op == CarOperation.ACCEL.value:
            car.changeSpeed(int(request[5:]), 1000)
            response = CarOperation.OK.encode("utf-8")
            next_client.send(request.encode("utf-8"))

        elif op == CarOperation.DECEL.value:
            next_client.send(request.encode("utf-8"))
            msg = next_client.recv(1024).decode("utf-8")
            
            if msg != CarOperation.OK.value:
                raise Exception("Does not receive OK from next car")
            
            if speed < 0 or speed > 1000: 
                raise Exception("Invalid speed")
            
            car.changeSpeed(speed, 1000)
            response = CarOperation.OK.encode("utf-8")

    except Exception as e:
        print(e)

next_client.close()
client_socket.close()
server.close()
