n = int(input())
nums = list(map(int, input().split()))
seen = set()
for x in nums:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)
