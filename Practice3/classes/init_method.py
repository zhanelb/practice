class Student:
    def __init__(self, name):
        self.name = name

s = Student("Zhanel")
print(s.name)


class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

r = Rectangle(3, 4)
print(r.w, r.h)


class Circle:
    def __init__(self, radius):
        self.radius = radius

c = Circle(5)
print(c.radius)
