#Sólo se ejecuta el primer patrón que coincide y también es capaz de extraer componentes


status = 418


def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
        
print(http_error(status))


# Los patrones pueden también verse como asignaciones que desempaquetan, y pueden usarse para ligar variables

point = (4 , 5)
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
    
    
# En este caso, el patrón (x, y) se usa para ligar las variables x e y a los valores de la tupla point.
#En este caso, el patrón Point(x=0, y=0) se usa para ligar las variables x e y a los valores de la instancia p.

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")   
    
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

p=Point(0 , 0)
where_is(p)




#Los patrones pueden anidarse arbitrariamente. Por ejemplo, si tuviéramos 
# una lista corta de puntos, con __match_args__ añadido, podríamos aplicar match así:

class Point:
    __match_args__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

points = [Point(0, 0), Point(1, 2)]


match points:
    case []:
        print("No points")
    case [Point(0, 0)]:
        print("The origin")
    case [Point(x, y)]:
        print(f"Single point {x}, {y}")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two on the Y axis at {y1}, {y2}")
    case _:
        print("Something else")
        
        
