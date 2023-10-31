# master jompi
import socket
from overdrive import Overdrive
from carEnum import CarOperation

# Police
car = Overdrive("FF:42:39:21:77:C3")

# they can connect more than 1 cars later :)
next_ip = "jopi.local"
port = 7956

next_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
next_client.connect((next_ip, port))

while True :
    try:
        request = input("Enter new command(close/accel/decel): ")
        op, speed = request.split()
        op = op.lower()
        speed = int(speed)

        if op == CarOperation.CLOSE.value:
            next_client.send(request.encode("utf-8"))
            break
        
        if op == CarOperation.ACCEL.value:
            next_client.send(request.encode("utf-8"))
            car.changeSpeed(speed, 1000)

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
