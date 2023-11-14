from car import Car

# slave1: skull
car = Car("D5:C7:94:15:78:8D", "kangbid.local", 7956, cur_ip="jopi.local", cur_port=7956)

while True:
    try:
        car.get_request()
    except Exception as e:
        print(e)
