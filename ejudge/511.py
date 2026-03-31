import re
text=input()
pat=re.compile(r"\w+")
words=pat.findall(text)
print(len(words))