import re
text=input()
res=re.match("^[A-Za-z].*[0-9]$",text)
if res:
    print("Yes")
else:
    print("No")
