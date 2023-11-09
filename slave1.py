import socket
from overdrive import Overdrive

car = Overdrive("D5:C7:94:15:78:8D")

# connect to master
cur_slave_ip = "jopi.local"
cur_slave_port = 7956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cur_slave_ip, cur_slave_port))
server.listen()
print(f"Listening on {cur_slave_ip}:{cur_slave_port}")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr[0]}:{addr[1]}")

# connect to next slave
nxt_slave_ip = "kangbid.local"
nxt_slave_port = 7956

cur_slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cur_slave.connect((nxt_slave_ip, nxt_slave_port))

def run_slave() :
    while True :
        command = client_socket.recv(1024).decode("utf-8")

        print(f"Received: {command}")

        if (command.lower() == "close") :
            cur_slave.send(command.encode("utf-8")[:1024])
            break

        operator = command
        if operator[0] == "S" :
            speed = int(operator.split()[1])
            if car.speed < speed :
                car.changeSpeed(speed, 100)
                cur_slave.send(command.encode("utf-8")[:1024])
            else :
                cur_slave.send(command.encode("utf-8")[:1024])
                while (cur_slave.recv(1024) != "accepted") :
                    pass
                if cur_slave.recv(1024) == "accepted" :
                    car.changeSpeed(speed, 100)
                    client_socket.send("accepted".encode("utf-8"))
        elif operator == "L" :
            car.changeLaneLeft(1000, 1000)
            cur_slave.send(command.encode("utf-8")[:1024])
        elif operator == "R" :
            car.changeLaneRight(1000, 1000)
            cur_slave.send(command.encode("utf-8")[:1024])

    car.disconnect()
    client_socket.close()
    print("Connection to client closed")
    server.close()
    cur_slave.close()
    
run_slave()
