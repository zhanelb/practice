with open("sample.txt", "r") as f:
    print("READ():")
    print(f.read())
with open("sample.txt", "r") as f:
    print("\nREADLINE():")
    print(f.readline())
with open("sample.txt", "r") as f:
    print("\nREADLINES():")
    print(f.readlines())