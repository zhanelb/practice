import re
text=input()
res=re.findall(r"\d",text)
print(" ".join(res))
