from car import Car

# slave2 : shock
car = Car("CE:71:D1:FC:B5:4F", "kangbid.local", 7956, cur_ip="jopi.local", cur_port=7956)

while True:
    try:
        car.get_request()
    except Exception as e:
        print(e)
