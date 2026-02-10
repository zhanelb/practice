def add(a, b):
    return a + b

print(add(10, 5))


def is_even(n):
    return n % 2 == 0

print(is_even(4))
print(is_even(7))


def min_max(nums):
    return min(nums), max(nums)

mn, mx = min_max([3, 8, 1, 5])
print(mn, mx)
