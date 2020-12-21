import datetime
import re

DEFAULT_ENCODING = "utf-8"
SUPPORTED_VERSION = ["1.0"]
USING_VERSION = "1.0"
HEAD_LENGTH = 100
STATUS_CODE_DICT = {
    200: "OK",
    301: "Moved Permanently",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    505: "Not Supported",
}
'''
shttp.py (simlar-http) contains the following functions:
    - parsing like-http packet
    - calling the data handler
    - replying the results by sending like-http packet

The format of my like-http is as follows:

1. Request message
    _______________________________________         ---+                    ----+
    |    [method]    |SPACE|[version]|CRLF|            | Request line           |
    |________________|_____|_________|____|__       ---+                        |
    |        host         |SPACE|[value]|CRLF|         |                        |
    |_____________________|_____|_______|____|         |                        |
    |    Authorization    |SPACE|[value]|              |                        |
    |_____________________|_____|_______|              |                        |
    |        Date         |SPACE|[value]|              | Header line            | 100 Bytes (fixed)
    |_____________________|_____|_______|              |                        |
    |  Content-Length     |SPACE|[value]|              |                        |
    |_____________________|_____|_______|           ---+                        |
    |SPACE| CRLF |                                     | Blank line             |
    |____ |______|____________ ______________       ---+                    ----+  
    |               Entity body              |         | request data
    |________________________________________|      ---+

    - method
        - DELETE    delete an object on the server
        - GET       request an object
        - HEAD      similar to the `GET` method, but it leaves out the requested object
        - POST      update an object
        - PUT       upload objects to the server
'''

def request_message(method, version="1.0", host='127.0.0.1', item_info=None):
    
    content_length, content = content_message(item_info)
    header = header_messsage(method, version, host, content_length)
    return  header + content


def header_messsage(method, version, host, Content_Length):
    date = str(datetime.datetime.now())
    head = "{0} {1}\nHost {2}\nAuthorization admin\nDate {3}\nContent-Length {4}\n".format(
        method, version, host, date, Content_Length)
    head += (HEAD_LENGTH - 1 - len(head)) * ' ' + '\n'
    return head.encode(DEFAULT_ENCODING)

def content_message(item_info):

    if item_info == None:
        return 0, b''
    content = ""
    binary_data = b''
    for key in item_info.keys():
        if key != "photo":
            content += key + ' ' + item_info[key] + '\n'
        else:
            binary_data = item_info["photo"]

    return len(content), content.encode(DEFAULT_ENCODING) + binary_data

def check_header(head_dict):
    error = False
    if head_dict["version"] not in SUPPORTED_VERSION:
        error = True
    if int(head_dict["status-code"]) not in STATUS_CODE_DICT:
        error = True
    return error

def response_parsing(mess):

    head = bytes.decode(mess[:HEAD_LENGTH])
    head_dict = {}
    head_lines = head.split('\n')

    head_dict["version"], head_dict["status-code"] = head_lines[0].split(' ')
    for line in head_lines[1:-2]:
        key, value = line.split(' ', 1)
        head_dict[key] = value

    error = check_header(head_dict)

    print("Just received from server:\n", "header:", head_dict)

    item_info = content_parsing(mess[HEAD_LENGTH:], int(head_dict["Content-Length"]))

    if error:
        head_dict["status-code"] = 505

    return int(head_dict["status-code"]), item_info

def content_parsing(content, decode_len):
    if len(content) == 0:
        return {}
    head = bytes.decode(content[:decode_len])
    item_info = {}

    items = head.split('\n')
    if len(items) == 1: # No item_info
        return items[0]
    for item in items:
        if(len(item) == 0):
            break
        key, value = item.split(' ', 1)
        item_info[key] = value
    print("item_info:", item_info)
    if "val_photo" in item_info and item_info["val_photo"] == "1":
        item_info["photo"] = content[decode_len:]


    return item_info