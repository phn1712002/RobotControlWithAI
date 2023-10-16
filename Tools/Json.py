import json, os
 
def loadJson(path='./config.json'):
    # Check path have file exist
    if os.path.exists(path):
        # Read path 
        with open(path, 'r') as json_file:
                data_save = json.load(json_file)
        return data_save
    else:
        return None
    

def saveJson(path='./config.json', data=None):
    # Save data in file 
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return True

    