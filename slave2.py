import socket
from overdrive import Overdrive

car = Overdrive("CE:71:D1:FC:B5:4F")

# connect to master
cur_slave_ip = "kangbid.local"
cur_slave_port = 7956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cur_slave_ip, cur_slave_port))
server.listen()
print(f"Listening on {cur_slave_ip}:{cur_slave_port}")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr[0]}:{addr[1]}")

def run_slave() :
    while True :
        command = client_socket.recv(1024).decode("utf-8")

        print(f"Received: {command}")

        if (command.lower() == "close") :
            break

        operator = command
        if operator == "" :
            break
        elif operator[0] == "S" :
            speed = int(int(operator.split()[1]) * 0.99159595)
            car.changeSpeed(speed, 100)
        elif operator == "L" :
            car.changeLaneLeft(1000, 1000)
        elif operator == "R" :
            car.changeLaneRight(1000, 1000)

    car.disconnect()
    client_socket.close()
    print("Connection to client closed")
    server.close()

run_slave()
