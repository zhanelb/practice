def string_to_number(s: str) -> int:
    digits = {
        "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
        "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
    }
    num_str = ""
    for i in range(0, len(s), 3):
        num_str += digits[s[i:i+3]]
    return int(num_str)
def number_to_string(n: int) -> str:
    rev = {
        "0": "ZER", "1": "ONE", "2": "TWO", "3": "THR", "4": "FOU",
        "5": "FIV", "6": "SIX", "7": "SEV", "8": "EIG", "9": "NIN"
    }
    if n == 0:
        return "ZER"
    res = ""
    for ch in str(n):
        res += rev[ch]
    return res
expr = input().strip()
op_pos = -1
op = ""
for symbol in "+-*":
    if symbol in expr:
        op = symbol
        op_pos = expr.index(symbol)
        break
left = expr[:op_pos]
right = expr[op_pos+1:]
a = string_to_number(left)
b = string_to_number(right)
if op == "+":
    ans = a + b
elif op == "-":
    ans = a - b
else:  
    ans = a * b
print(number_to_string(ans))
