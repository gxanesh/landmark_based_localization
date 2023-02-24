# Python program to read
# json file


import json

# Opening JSON file
filepath = '../localization/data/landmark_data.json'
f = open(filepath)

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data:
    print(i)

# Closing file
f.close()
