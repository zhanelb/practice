n = int(input())
surnames = []
for i in range(n):
    surnames.append(input())
unique = set(surnames)
print(len(unique))
