import re
text = input()
res = re.findall(r"\b[A-Za-z]{3}\b", text)
print(len(res))