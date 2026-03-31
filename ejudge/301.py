def is_valid(n):
    while n>0:
        digit=n%10
        if digit % 2 !=0:
            return False
        n//=10
    return True
n=int(input())
if is_valid(n):
    print("Valid")
else:
    print("Not valid")