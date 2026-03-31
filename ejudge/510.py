import re
text=input()
r=re.findall(r"cat|dog",text)
if r:
    print("Yes")
else:
    print("No")