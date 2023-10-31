from car import Car

car = Car("FF:42:39:21:77:C3", "jopi.local", 7956)

while True:
    try:
        car.get_input()
    except Exception as e:
        print(e)
    
