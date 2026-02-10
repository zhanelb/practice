
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, I am", self.name)

p = Person("Aruzhan")
p.say_hello()


class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
print(calc.add(2, 3))


class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

cnt = Counter()
cnt.inc()
cnt.inc()
print(cnt.value)
