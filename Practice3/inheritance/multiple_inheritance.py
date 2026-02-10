class A:
    def a(self):
        print("A")

class B:
    def b(self):
        print("B")

class C(A, B):
    pass

c = C()
c.a()
c.b()


class Flyer:
    def move(self):
        print("Flying")

class Swimmer:
    def move(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass

Duck().move()  


class X:
    def hi(self):
        print("Hi from X")

class Y:
    def hi(self):
        print("Hi from Y")

class Z(Y, X):
    pass

Z().hi()
