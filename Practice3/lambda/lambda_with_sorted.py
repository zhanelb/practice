nums = [5, 2, 9, 1]
print(sorted(nums))

words = ["banana", "fig", "apple", "kiwi"]
print(sorted(words, key=lambda w: len(w)))

pairs = [("a", 3), ("b", 1), ("c", 2)]
print(sorted(pairs, key=lambda p: p[1]))
