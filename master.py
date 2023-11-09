import socket
from overdrive import Overdrive

def run_master() :
    while True :
        command = input("Enter Command : ")

        if command == "close" :
            master.send(command.encode("utf-8")[:1024])
            break

        operator = command
        if operator[0] == "S" :
            speed = int(int(operator.split()[1]) * 0.988725)
            if car.speed < speed :
                car.changeSpeed(speed, 100)
                master.send(command.encode("utf-8")[:1024])
            else :
                master.send(command.encode("utf-8")[:1024])
                while master.recv(1024) != "accepted" :
                    pass
                car.changeSpeed(speed, 100)
        elif operator == "L" :
            car.changeLaneLeft(988.725, 1000)
            master.send(command.encode("utf-8")[:1024])
        elif operator == "R" :
            car.changeLaneRight(988.725, 1000)
            master.send(command.encode("utf-8")[:1024])
    car.disconnect()
    master.close()
    print("Connection to server closed")

# overdrive_mac_address = input("Enter Overdrive MAC address: ")
overdrive_mac_address = "C4:AA:03:6B:22:FA"
car = Overdrive(overdrive_mac_address)

# Input Format : "ip port"
# slave1_ip, slave1_port = input("Enter next slave IP address and port number: ").split()
slave1_ip, slave1_port = "jopi.local 7956".split()
slave1_port = int(slave1_port)

master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master.connect((slave1_ip, slave1_port))

run_master()
