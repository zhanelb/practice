import re
text=input()
p=input()
res=re.split(p,text)
print(",".join(res))