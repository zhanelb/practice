import re
text = input()
if re.fullmatch(r"\b^[A-Z]+[a-z]+\b", text):
    print("Match")