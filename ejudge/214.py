n = int(input())
nums = list(map(int, input().split()))
max_count = 0
ans = nums[0]
for i in range(n):
    count = 0
    for j in range(n):
        if nums[j] == nums[i]:
            count += 1
    if count > max_count:
        max_count = count
        ans = nums[i]
    elif count == max_count and nums[i] < ans:
        ans = nums[i]
print(ans)
