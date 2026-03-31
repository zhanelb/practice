n=int(input())
num=list(map(int,input().split()))
num.sort(reverse=True)
for i in num:
    print(i,end=" ")