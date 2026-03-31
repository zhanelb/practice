n=int(input())
num=list(map(int,input().split()))
for i in num:
    i*=i
    print(i,end=" ")