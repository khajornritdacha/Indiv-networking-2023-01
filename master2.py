from car import Car
from carEnum import CarOperation

car = Car("FF:42:39:21:77:C3", "jopi.local", 7956)

while True:
    try:
        res = car.get_input()
        print(res)
        if res == CarOperation.CLOSE.value:
            break
    except Exception as e:
        print(e)
    
