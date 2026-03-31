import re
text=input()
res=re.search(r"\S+@\S+\.\S+",text)
if res:
    print(res.group())
else:
    print("No email")