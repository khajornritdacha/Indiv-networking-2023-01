import socket
from overdrive import Overdrive
from carEnum import CarOperation

class Car:
    def __init__(self, car_mac_addr, next_ip, next_port, **kwargs):
        self.car = Overdrive(car_mac_addr)
        
        self.car_mac_addr = car_mac_addr
        self.next_ip = next_ip
        self.next_port = next_port
        self.cur_ip = None
        self.cur_port = None
        self.server = None
        self.factor = 1.0

        if "factor" in kwargs:
            self.factor = kwargs["factor"]

        if self.next_ip is not None and self.next_port is not None:
            self.next_car = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.next_car.connect((self.next_ip, self.next_port))
            print(f"Connected to {self.next_ip}:{self.next_port}")

        if "cur_ip" in kwargs and "cur_port" in kwargs:
            self.cur_ip = kwargs["cur_ip"]
            self.cur_port = kwargs["cur_port"]
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.cur_ip, self.cur_port))
            self.server.listen()
            print(f"Listening on {self.cur_ip}:{self.cur_port}")

            prev_car, addr = self.server.accept()
            self.prev_car = prev_car
            print(f"Prev car: {self.prev_car}")
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

    def parse_request(self, request):
        print(f"{self.car_mac_addr}: {request}")
        try:
            op, speed = request.strip().split()
            op = int(op.lower())
            speed = int(speed)
            print(f"OP: {op}, speed: {speed}")
            return op, speed
        except Exception as e:
            print(e)
        
    def handle_close(self):
        if self.next_car is not None:
            self.next_car.send(CarOperation.CLOSE.value.encode("utf-8"))
            
    def handle_accel(self, request, speed):
        self.car.changeSpeed(int(speed * self.factor), 1000)
        if self.next_car is None:
            return
        self.next_car.send(request.encode("utf-8"))

    def handle_decel(self, request, speed):
        if self.next_car is not None:
            self.next_car.send(request.encode("utf-8"))
            msg = self.next_car.recv(1024).decode("utf-8")
            print(f"Msg from prev: {msg}")
            if msg is not CarOperation.OK.value:
                print("Does not receive OK from next car")
                # raise Exception("Does not receive OK from next car")
        
        if speed < 0 or speed > 1000: 
            raise Exception("Invalid speed")
        self.car.changeSpeed(int(speed * self.factor), 1000)
        
        print(f"Prev car: {self.prev_car}")
        if self.prev_car is not None:
            self.prev_car.send(CarOperation.OK.value.encode("utf-8"))

    def handle_change_lane_left(self, request, speed):
        self.car.changeLaneLeft(speed, 1000)
        if self.next_car is None:
            return
        self.next_car.send(request.encode("utf-8"))

    def handle_change_lane_right(self, request, speed):
        self.car.changeLaneRight(speed, 1000)
        if self.next_car is None:
            return
        self.next_car.send(request.encode("utf-8"))

    def handle_request(self, request): 
        op, speed = self.parse_request(request)
        if op == 0:
            self.handle_close()
        elif op == 1:
            self.handle_accel(request, speed)
        elif op == 2:
            self.handle_decel(request, speed)
        elif op == 3:
            self.handle_change_lane_left(request, speed)
        elif op == 4:
            self.handle_change_lane_right(request, speed)
        else:
            raise Exception("Invalid operation")
        return op
    
    def get_input(self):
        request = input("""Enter new command
                        0 : to close
                        1 x : to accel with speed x
                        2 x : to decel with speed x
                        3 x : to change lane left with speed x
                        4 x : to change lane right with speed x
                        Input: """)
        return self.handle_request(request)

    def get_request(self):
        if self.prev_car is None: return
        request = self.prev_car.recv(1024).decode("utf-8")
        print(f"Received request: {request}")
        self.handle_request(request)
        
    def __del__(self):
        self.prev_car.close()
        self.next_car.close()
        self.server.close()