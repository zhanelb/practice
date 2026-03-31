n = int(input())
nums = input().split()
mx = int(nums[0])
for i in range(1, n):
    x = int(nums[i])
    if x > mx:
        mx = x

print(mx)
