def Powers_of_Two(n):
    for i in range(n+1):
        yield 2**i
n=int(input())
for j in Powers_of_Two(n):
    print(j,end=" ")