import threading
import csv, os, shutil
import socket


'''
    Database organization structure

    |- data
        |- student
            |- 00001
                |- 00001.jpg
                |- 00001.csv 
            |- 00002
                |- 00002.jpg
                |- 00002.csv 
            .
            .
                .
'''

DATA_DIR = ".\\data\\student\\"

# All information about a `item` includes:
# columns of a CSV file: [id] [name] [val_photo]
# , and a photo stored in the same directory
DEFAULT_ITEM = {
    'id': None,
    'name': "No name",
    'val_photo': '2',
    'photo': None
}
# Read an item from disk and return it.
def read_item(item_id):
    item_path = DATA_DIR + item_id + "\\"
    item_info =  {
    'id': None,
    'name': "No name",
    'val_photo': '0',
    'photo': None
    }
    if os.path.exists(item_path):
        with open(item_path + '{}.csv'.format(item_id), 'r') as f:
            reader = csv.reader(f)
            i = 0
            for item in reader:
                if i == 0 and item[0] == item_id:
                    i += 1
                    item_info['id'] = item[0]
                    item_info['name'] = item[1]
                    item_info['val_photo'] = item[2]
                    if(item_info['val_photo'] == '1'):
                        with open(item_path + '{}.jpg'.format(item_id), "rb") as f:
                            item_info['photo'] = f.read()
                else:
                    break
    return item_info

# Write an item into disk
def write_item(item_info):
    
    with open(DATA_DIR + "{0}\\{0}.csv".format(item_info['id']), 'w')  as f:
        writer = csv.writer(f)
        csv_data = [item_info['id'], item_info['name'], item_info['val_photo']]
        writer.writerow(csv_data)
    if item_info['val_photo'] == "1":
        with open(DATA_DIR + "{0}\\{0}.jpg".format(item_info['id']), "wb") as f:
            f.write(item_info['photo'])

# Get an item info by `read_item()`
def get_item_handler(item_info):
    item_info = read_item(item_info['id'])
    if item_info['id']:
        print(item_info)
    else:
        return "Non-existent"

# Delete an item floder
def delete_item_handler(item_info):
    item_path = DATA_DIR + item_info['id'] + "\\"
    if os.path.exists(item_path):
        shutil.rmtree(item_path)
    else:
        return "Non-existent"

# Add a new item by `write_item()`
def add_item_handler(item_info):

    item_path = DATA_DIR + item_info['id'] + "\\"
    if not os.path.exists(item_path):
        os.mkdir(item_path)
        write_item(item_info)
    else:
        return "Already exists"

# Update an item by `write_item()`
def update_item_handler(item_info):
    item_path = DATA_DIR + item_info['id'] + "\\"
    if not os.path.exists(item_path):
        return "Non-existent"

    item_dict = read_item(item_info['id'])

    for key in item_info.keys():
        if item_info[key] != DEFAULT_ITEM[key]:
            item_dict[key] = item_info[key]
    write_item(item_dict)

# Check to see if `item_info` is valid 
def check_item_info(item_info):

    for key in DEFAULT_ITEM.keys():
        if key not in item_info:
            item_info[key] = DEFAULT_ITEM[key]
    
    if len(item_info) != len(DEFAULT_ITEM) or \
        item_info['id'] == None:
        return False

    if (item_info['val_photo'] == '1' and not item_info['photo']) or \
        (item_info['photo'] and item_info['val_photo'] == '0'):
        return False
    
    return True

# The entry function (for threads) to process client requests
def handler(instr, item_info):
    mess = ''
    if not check_item_info(item_info) or \
        instr not in HANDLER_FUNC_DICT:
        mess =  "Invalid values"
    else:
        mess  = HANDLER_FUNC_DICT[instr](item_info)
    print("mess: ", mess)

HANDLER_FUNC_DICT = {

    'delete': delete_item_handler,
    'add': add_item_handler,
    'get': get_item_handler,
    'update': update_item_handler,
}

item_info = {
        'id' : "00005",
        'name': "Sandy",
        'val_photo': '1'
}

with open("xxx.jpg", 'rb') as f:
    reader = f.read()
    item_info['photo'] = reader

handler("get", item_info)