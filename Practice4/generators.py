#1
def square_generator(n):
    for i in range(n+1):
        yield i*i

n = int(input())
for j in square_generator(n):
    print(j)
#2
def even_numbers(p):
    for i in range(p+1):
        if i%2==0:
            yield i
p=int(input())
print(",".join(map(str,even_numbers(p))))
#3
def divisible(n):
    for i in range(n+1):
        if i%3==0 and i%4==0:
            yield i
n=int(input())
for j in divisible(n):
    print(j)
#4
def squares(a, b):
    for i in range(a,b+1):
        yield i*i
a=int(input())
b=int(input())
for j in squares(a,b):
    print(j)
#5
def countdown(n):
    for i in range(n,-1,-1):
        yield i
n=int(input())
for j in countdown(n):
    print(j)