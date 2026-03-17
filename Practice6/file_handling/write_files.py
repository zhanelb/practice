with open("sample.txt", "w") as f:
    f.write("Hello\n")
    f.write("Python\n")
with open("sample.txt", "a") as f:
    f.write("Appended line\n")
with open("sample.txt", "r") as f:
    print(f.read())