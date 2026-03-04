s = input()
parts = s.split("_")
res = parts[0]
for p in parts[1:]:
    res += p.capitalize()
print(res)