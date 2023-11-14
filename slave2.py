import socket
import time
from overdrive import Overdrive

# ------------------------------------ Variables ------------------------------------- #

slave1_client = None

slave2_mac_address = None
slave2_car = None
slave2_server = None
slave2_ip = None
slave2_port = None
slave2_client = None

def setup_self():

    global slave1_client
    global slave2_mac_address, slave2_car, slave2_server
    global slave2_ip, slave2_port

    slave2_mac_address = "CE:71:D1:FC:B5:4F"
    slave2_car = Overdrive(slave2_mac_address)

    slave2_ip, slave2_port = "kangbid.local", 7956

    slave2_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slave2_server.bind((slave2_ip, slave2_port))
    slave2_server.listen()
    print(f"Listening on {slave2_ip}:{slave2_port}")

    slave1_client, addr = slave2_server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

# ------------------------------------------------------------------------------------ #

def run():

    global slave1_client
    global slave2_mac_address, slave2_car, slave2_ip, slave2_port, slave2_server, slave2_client
    global slave2_ip, slave2_port

    while True:
        command = slave1_client.recv(1024).decode("utf-8")

        print(f"Received: {command}")

        command_encoded = command.encode("utf-8")[:1024]

        if command.lower() == "close":
            slave2_client.send(command_encoded)
            break

        opr = command
        if opr == "":
            break
        elif opr[0] == "C":
            speed = int(opr.split()[1])
            if slave2_car.speed < speed:
                slave2_car.changeSpeed(speed, 100)
                slave2_client.send(command_encoded)
            else:
                slave2_client.send(command_encoded)
                time.sleep(0.1)
                slave2_car.changeSpeed(speed, 100)
        elif opr == "R":
            slave2_car.changeLaneRight(1000, 1000)
            slave2_client.send(command_encoded)
        elif opr == "L":
            slave2_car.changeLaneLeft(1000, 1000)
            slave2_client.send(command_encoded)    

# ------------------------------------------------------------------------------------ #

def close():
    global slave1_client
    global slave2_car, slave2_client, slave2_server

    slave2_car.disconnect()
    slave1_client.close()
    print("Connection to client closed")
    slave2_server.close()

# --------------------------------------- Main -----------------------------------------------#

setup_self()
run()
close()