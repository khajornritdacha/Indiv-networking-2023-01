import socket
import time
from overdrive import Overdrive

# ------------------------------------ Variables ------------------------------------- #

master_mac_address = None
master_car = None
master_client = None

slave1_ip = None
slave1_port = None

def setup_self():

    global master_mac_address, master_car, master_client
    global slave1_ip, slave1_port

    master_mac_address = "C4:AA:03:6B:22:FA"
    master_car = Overdrive(master_mac_address)

    slave1_ip, slave1_port = "jopi.local", 7956
    slave1_port = int(slave1_port)

    master_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_client.connect((slave1_ip, slave1_port))

# ------------------------------------------------------------------------------------ #

def run():

    global master_car, master_client

    while True:
        user_input = input("Please enter command: ")  # Get user's command

        command_encoded = user_input.encode("utf-8")[:1024]

        if user_input == "exit":
            master_client.send(command_encoded)
            break

        opr = user_input
        if opr[0] == "C":  # Change Speed
            new_speed = int(int(opr.split()[1]) * 0.988725)
            current_speed = master_car.speed
            if current_speed < new_speed:
                master_car.changeSpeed(new_speed, 100)
                master_client.send(command_encoded)
            else:
                master_client.send(command_encoded)
                time.sleep(0.2)
                master_car.changeSpeed(new_speed, 100)
        elif opr == "R":  # Change Lane Right
            master_car.changeLaneRight(1000, 1000)
            master_client.send(command_encoded)
        elif opr == "L":  # Change Lane Left
            master_car.changeLaneLeft(1000, 1000)
            master_client.send(command_encoded)

# ------------------------------------------------------------------------------------ #

def close():

    global master_car, master_client

    master_car.disconnect()
    master_client.close()
    print("Server connection closed")

# --------------------------------------- Main -----------------------------------------------#

setup_self()
run()
close()