n = int(input())
m1 = map(int, input().split())
m2 = map(int, input().split())
res = 0
for a, b in zip(m1, m2):
    res += a * b
print(res)