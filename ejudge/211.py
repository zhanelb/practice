n, l, r = map(int, input().split())
nums = list(map(int, input().split()))
l -= 1
r -= 1
while l < r:
    nums[l], nums[r] = nums[r], nums[l]
    l += 1
    r -= 1
for x in nums:
    print(x, end=" ")
