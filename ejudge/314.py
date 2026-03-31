n = int(input())
arr = list(map(int, input().split()))
q = int(input())
for _ in range(q):
    operation = input().split()
    if operation[0] == "add":
        x = int(operation[1])
        func = lambda a: a + x
    elif operation[0] == "multiply":
        x = int(operation[1])
        func = lambda a: a * x
    elif operation[0] == "power":
        x = int(operation[1])
        func = lambda a: a ** x
    elif operation[0] == "abs":
        func = lambda a: abs(a)
    arr = list(map(func, arr))
print(*arr)
