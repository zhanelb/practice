
class Animal:
    def speak(self):
        print("...")

class Dog(Animal):
    def speak(self):
        print("Woof")

Dog().speak()


class Parent:
    def show(self):
        print("Parent")

class Child(Parent):
    def show(self):
        print("Child")

Child().show()


class Vehicle:
    def move(self):
        print("Moving")

class Bike(Vehicle):
    def move(self):
        print("Biking")

Bike().move()
