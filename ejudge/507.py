import re
text=input()
pat=input()
rep=input()
res=re.sub(pat,rep,text)
print(res)