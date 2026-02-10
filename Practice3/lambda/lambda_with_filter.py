nums = [1, 2, 3, 4, 5, 6]
print(list(filter(lambda x: x % 2 == 0, nums)))


words = ["hi", "python", "ok", "lesson"]
print(list(filter(lambda w: len(w) > 2, words)))


temps = [-3, 0, 5, -1, 8]
print(list(filter(lambda t: t >= 0, temps)))
