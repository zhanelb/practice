class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()


class Bird(Animal):
    def speak(self):
        print("Chirp")

b = Bird()
b.speak()


class Cat(Animal):
    def speak(self):
        print("Meow")

c = Cat()
c.speak()
