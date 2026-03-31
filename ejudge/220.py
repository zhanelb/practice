import sys
n = int(sys.stdin.readline())
db = {}
for _ in range(n):
    line = sys.stdin.readline().rstrip()
    parts = line.split(maxsplit=2)
    if parts[0] == "set":
        key = parts[1]
        value = parts[2] if len(parts) > 2 else ""
        db[key] = value
    elif parts[0] == "get":
        key = parts[1]
        if key in db:
            print(db[key])
        else:
            print(f"KE: no key {key} found in the document")
