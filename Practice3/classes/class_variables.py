class School:
    city = "Almaty"

print(School.city)


class Student:
    school_name = "PP2 School"
    def __init__(self, name):
        self.name = name

a = Student("Ali")
b = Student("Dana")
print(a.school_name)
print(b.school_name)


Student.school_name = "New School"
print(a.school_name)
print(b.school_name)
