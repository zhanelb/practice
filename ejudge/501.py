import re
text=input()
res=re.match("Hello",text)
if res:
    print("Yes")
else:
    print("No")
