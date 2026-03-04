import re
s = input()
res=re.sub(r"([A-Z])", r"_\1", s).lower()
print(res)