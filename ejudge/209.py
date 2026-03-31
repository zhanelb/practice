n = int(input())
nums = list(map(int, input().split()))
mx = nums[0]
mn = nums[0]
for i in range(1, n):
    if nums[i] > mx:
        mx = nums[i]
    if nums[i] < mn:
        mn = nums[i]
for i in range(n):
    if nums[i] == mx:
        nums[i] = mn
for x in nums:
    print(x, end=" ")
