from socket import socket
from overdrive import Overdrive
from carEnum import CarOperation

class Car:
    def __init__(self, car_mac_addr, next_ip, next_port, **kwargs):
        self.car = Overdrive(car_mac_addr)
        
        self.next_ip = next_ip
        self.next_port = next_port
        self.cur_ip = None
        self.cur_port = None
        self.server = None

        self.next_car = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.next_car.connect((self.next_ip, self.next_port))
        print(f"Connected to {self.next_ip}:{self.next_port}")

        if "cur_ip" and "cur_port" in kwargs:
            self.cur_ip = kwargs["cur_ip"]
            self.cur_port = kwargs["cur_port"]
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.cur_ip, self.cur_port))
            self.server.listen()
            print(f"Listening on {self.cur_ip}:{self.cur_port}")

            self.prev_car, addr = self.server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

    def parse_request(self, request):
        op, speed = request.split()
        op = op.lower()
        speed = int(speed)
        return op, speed

    def handle_close(self):
        if self.next_car is not None:
            self.next_car.send(CarOperation.CLOSE.value.encode("utf-8"))
            
    def handle_accel(self, request, speed):
        if self.next_car is None:
            return
        self.car.changeSpeed(speed, 1000)
        self.next_car.send(request.encode("utf-8"))

    def handle_decel(self, request, speed):
        if self.next_car is not None:
            self.next_car.send(request.encode("utf-8"))
            msg = self.next_car.recv(1024).decode("utf-8")
            if msg is not CarOperation.OK.value:
                raise Exception("Does not receive OK from next car")
        
        if speed < 0 or speed > 1000: 
            raise Exception("Invalid speed")
        self.car.changeSpeed(speed, 1000)
        
        if self.prev_car is not None:
            self.prev_car.send(CarOperation.OK.value.encode("utf-8"))

    def get_input(self):
        try:
            request = input("Enter new command(close/accel/decel): ")
            op, speed = self.parse_request(request)

            match op:
                case CarOperation.CLOSE.value:
                    self.handle_close()
                case CarOperation.ACCEL.value:
                    self.handle_accel(request, speed)
                case CarOperation.DECEL.value:
                    self.handle_decel(request, speed)
                case _:
                    raise Exception("Invalid operation")
        except Exception as e:
            print(e)
    
    def get_request(self):
        try:
            request = self.prev_car.recv(1024).decode("utf-8")
            op, speed = self.parse_request(request)

            match op:
                case CarOperation.CLOSE.value:
                    self.handle_close()
                case CarOperation.ACCEL.value:
                    self.handle_accel(request, speed)
                case CarOperation.DECEL.value:
                    self.handle_decel(request, speed)
                case _:
                    raise Exception("Invalid operation")

        except Exception as e:
            print(e)

    def __del__(self):
        self.prev_car.close()
        self.next_car.close()
        self.server.close()