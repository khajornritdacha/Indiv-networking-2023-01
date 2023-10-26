# master jompi
import socket
from overdrive import Overdrive

# Police
car = Overdrive("FF:42:39:21:77:C3")

# they can connect more than 1 cars later :)
ip = "jopi.local"
port = 7956

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

while True :
    try:
        new_speed = input("Enter new speed : ")

        if new_speed == "close" :
            break

        client.send(new_speed.encode("utf-8")[:1024])

        speed = int(new_speed[5:])
        car.changeSpeed(speed, 1000)
    except Exception as e:
        print(e)

client.close()
