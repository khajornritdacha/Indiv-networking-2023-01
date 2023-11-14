import socket
import time
from overdrive import Overdrive

# ------------------------------------ Variables ------------------------------------- #

master_client = None

slave1_mac_address = None
slave1_car = None
slave1_server = None
slave1_ip = None
slave1_port = None
slave1_client = None

slave2_ip = None 
slave2_port = None

def setup_self():

    global master_client
    global slave1_mac_address, slave1_car, slave1_server
    global slave1_ip, slave1_port

    slave1_mac_address = "D5:C7:94:15:78:8D"
    slave1_car = Overdrive(slave1_mac_address)

    slave1_ip, slave1_port = "jopi.local", 7956

    slave1_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slave1_server.bind((slave1_ip, slave1_port))
    slave1_server.listen()
    print(f"Listening on {slave1_ip}:{slave1_port}")

    master_client, addr = slave1_server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

def setup_slave2():
    
    global slave1_mac_address, slave1_car, slave1_ip, slave1_port, slave1_client
    global slave2_ip, slave2_port

    slave2_ip, slave2_port = "kangbid.local", 7956

    slave1_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slave1_client.connect((slave2_ip, slave2_port))

# ------------------------------------------------------------------------------------ #

def run():

    global master_client
    global slave1_mac_address, slave1_car, slave1_ip, slave1_port, slave1_server, slave1_client
    global slave2_ip, slave2_port

    while True:
        command = master_client.recv(1024).decode("utf-8")

        print(f"Received: {command}")

        command_encoded = command.encode("utf-8")[:1024]

        if command.lower() == "close":
            slave1_client.send(command_encoded)
            break

        opr = command
        if opr == "":
            break
        elif opr[0] == "C":
            speed = int(opr.split()[1])
            if slave1_car.speed < speed:
                slave1_car.changeSpeed(speed, 100)
                slave1_client.send(command_encoded)
            else:
                slave1_client.send(command_encoded)
                time.sleep(0.1)
                slave1_car.changeSpeed(speed, 100)
        elif opr == "R":
            slave1_car.changeLaneRight(1000, 1000)
            slave1_client.send(command_encoded)
        elif opr == "L":
            slave1_car.changeLaneLeft(1000, 1000)
            slave1_client.send(command_encoded)    

# ------------------------------------------------------------------------------------ #

def close():
    global master_client
    global slave1_car, slave1_client, slave1_server

    slave1_car.disconnect()
    master_client.close()
    print("Connection to client closed")
    slave1_server.close()
    slave1_client.close()

# --------------------------------------- Main -----------------------------------------------#

setup_self()
setup_slave2()
run()
close()