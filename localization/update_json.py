import json

# def create_json(filepath='../localization/data/landmark_data.json')
def create_json(filepath, fileName, data):
    filePathNameWExt = filepath + '/' + fileName + '.json'

    with open(filePathNameWExt, 'a') as fp:
        json.dump(data, fp, indent=1)
        fp.write(data)


def update_json(**kwargs ):
    # name = None, distance = None, location = None, ts = None
    filepath = '../localization/data/landmark_data.json'
    file = open(filepath, 'r+')
        # First we load existing data into a dict.
    file_data = json.load(file)
    # print(file_data)
        # Join new_data with file_data inside emp_details
    for key, value in kwargs.items():
        if key == "name":
            file_data['name'].append(value)
        elif key == "location":
            if value is None:
                file_data["location"].append(list((0,0)))
            else:
                file_data["location"].append(value)
        elif key == "distance":
            file_data['distance'].append(value)
        elif key == "timestamp":
            file_data["timestamp"].append(value)
    file.close()

    # convert back to json
    jsonFile =  open(filepath, "w+")
    json.dump(file_data, jsonFile,indent = 0)
    jsonFile.close()


def clear_json():
    filepath = '../localization/data/landmark_data.json'
    file = open(filepath, 'r+')
    # First we load existing data into a dict.
    file_data = json.load(file)
    file_data['name']       = []
    file_data["location"]   = []
    file_data['distance']   = []
    file_data["timestamp"]  = []

    jsonFile = open(filepath, "w+")
    json.dump(file_data, jsonFile, indent=0)
    print("JSON file cleared!")
    jsonFile.close()

# update_json(timestamp = 20.5)
# clear_json()

