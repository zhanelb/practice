import math
class Circle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return math.pi * self.r ** 2
r = int(input())
c = Circle(r)
print(f"{c.area():.2f}")
