import re
text = input()
if re.fullmatch(r"[a-z]+_[a-z]+", text):
    print("Match")