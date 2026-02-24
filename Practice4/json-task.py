import json
with open("sample-data.json", "r") as file:
    data = json.load(file)
print("Total count:", data["totalCount"])
for item in data["imdata"]:
    print("Interface ID:", item["l1PhysIf"]["attributes"]["id"])

