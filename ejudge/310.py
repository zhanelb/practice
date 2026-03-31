class person:
    def __init__(self, n):
        self.n = n
class student(person):
    def __init__(self,n,gpa):
        super().__init__(n)
        self.gpa = gpa
    def display(self):
        print(f"Student: {self.n}, GPA: {self.gpa}")
n,gpa=input().split()
gpa = float(gpa)
s = student(n, gpa)
s.display()