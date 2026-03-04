import re
s = input()
res=re.sub(r"([A-Z])", r" \1", s).strip()
print(res)