from car import Car
from carEnum import CarOperation

# master : big bang
car = Car("C4:AA:03:6B:22:FA", "jopi.local", 7956)

while True:
    try:
        res = car.get_input()
        print(res)
        if res == CarOperation.CLOSE.value:
            break
    except Exception as e:
        print(e)
    
