n = int(input())
a = list(map(int, input().split()))
s = 0
for x in a:
    if(x>0):
        s+=1
    else:
        continue
print(s)
