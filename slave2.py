from car import Car

# slave2 : shock
car = Car("CE:71:D1:FC:B5:4F", None, None, cur_ip="kangbid.local", cur_port=7956, factor=0.99159595)

while True:
    try:
        car.get_request()
    except Exception as e:
        print(e)
