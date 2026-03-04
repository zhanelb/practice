import re
s = input()
res=re.findall(r"[A-Z][a-z]*", s)
print(res)