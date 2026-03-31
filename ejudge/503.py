import re
text=input()
subs=input()
total=0
for i in re.finditer(subs,text):
    total+=1
print(total)
