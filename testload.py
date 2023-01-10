import json

with open("levels.json", "r+") as document:
    all_levels = json.load(document)
    print(all_levels)
    for level in all_levels:
        print(f"Name: {level[0]}")
        for line in level[1]:
            print(line)