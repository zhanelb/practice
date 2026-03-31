import re
text=input()
subs=input()
res=re.search(subs,text)
if res:
    print("Yes")
else:
    print("No")
