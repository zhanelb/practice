n = int(input())
freq = {}
for i in range(n):
    number = input()
    if number in freq:
        freq[number] += 1
    else:
        freq[number] = 1
count = 0
for v in freq.values():
    if v == 3:
        count += 1
print(count)
