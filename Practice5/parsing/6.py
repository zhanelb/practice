import re
text = input()
res = re.sub(r"[ ,.]", ":", text)
print(res)