class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Zhanel", 1)
print(s.name, s.grade)


class A:
    def hello(self):
        print("Hello from A")

class B(A):
    def hello(self):
        super().hello()
        print("Hello from B")

B().hello()


class Shape:
    def __init__(self, color):
        self.color = color

class Square(Shape):
    def __init__(self, color, side):
        super().__init__(color)
        self.side = side

sq = Square("red", 4)
print(sq.color, sq.side)
