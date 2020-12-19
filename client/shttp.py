import datetime

DEFAULT_ENCODING = "utf-8"
SUPPORTED_VERSION = ["1.0"]
USING_VERSION = "1.0"
HEAD_LENGTH = 100
STATUS_CODE_DICT = {
    200: "OK",
    301: "Moved Permanently",
    400: "Bad Request",
    401: "Unauthorized",
    404: "NotFound",
    505: "NotSupported",
}
'''
shttp.py (simlar-http) contains the following functions:
    - parsing like-http packet
    - calling the data handler
    - replying the results by sending like-http packet

The format of my like-http is as follows:

1. Request message
    _______________________________________         ---+
    |    [method]    |SPACE|[version]|CRLF|            | Request line
    |________________|_____|_________|____|__       ---+
    |        host         |SPACE|[value]|CRLF|         |
    |_____________________|_____|_______|____|         |
    |    Authorization    |SPACE|[value]|              |
    |_____________________|_____|_______|              |
    |        Date         |SPACE|[value]|              | Header line
    |_____________________|_____|_______|              |
    |  Content-Length     |SPACE|[value]|              |
    |_____________________|_____|_______|           ---+
    |CRLF|                                             | Blank line
    |____|___________________________________       ---+
    |               Entity body              |         | request data
    |________________________________________|      ---+

    - method
        - DELETE    delete an object on the server
        - GET       request an object
        - HEAD      similar to the `GET` method, but it leaves out the requested object
        - POST      update an object
        - PUT       upload objects to the server
'''

def request_message(method, version="1.0", host='127.0.0.1', content=""):
    date = str(datetime.datetime.now())
    head = "{0} {1}\nHost {2}\nAuthorization admin\nDate {3}\nContent-Length {4}\n".format(
        method, version, host, date, len(content))
    head += (HEAD_LENGTH - 1 - len(head)) * ' ' + '\n'
    mess = head + content
    return mess



def check_header(head_dict):
    error = False
    if head_dict["version"] not in SUPPORTED_VERSION:
        error = True
    if int(head_dict["status-code"]) not in STATUS_CODE_DICT:
        error = True
    return error

def response_parsing(mess):
    print("parsing...")

    head = bytes.decode(mess[:HEAD_LENGTH])
    head_dict = {}
    head_lines = head.split('\n')

    head_dict["version"], head_dict["status-code"] = head_lines[0].split(' ')
    for line in head_lines[1:-2]:
        key, value = line.split(' ', 1)
        head_dict[key] = value
    print(head_dict)

    error = check_header(head_dict)

    item_info = content_parsing(mess[HEAD_LENGTH:], int(head_dict["Content-Length"]))
    
    print(item_info)
    
    return error, STATUS_CODE_DICT[int(head_dict["status-code"])], item_info

def content_parsing(content, decode_len):
    head = bytes.decode(content[:decode_len])
    item_info = {}

    items = head.split('\n')
    for item in items:
        if(len(item) == 0):
            break
        key, value = item.split(' ', 1)
        item_info[key] = value
    if "photo" in item_info:
        item_info["photo"] = content[decode_len:]

    return item_info