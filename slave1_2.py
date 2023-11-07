from car import Car

# slave2 : shock
car = Car("CE:71:D1:FC:B5:4F", "jopi.local", 7956, cur_ip="jopi.local", cur_port=7955)

while True:
    try:
        car.get_request()
    except Exception as e:
        print(f"Error occur: {e}")
