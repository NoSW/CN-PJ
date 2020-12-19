from typing import ItemsView
from handler import handler
from thread import *
import datetime
import socket



MAXSIZE_BUFF = 1024*1024
MAX_LATENCY = 500000
DEFAULT_ENCODING = "utf-8"
STATUS_CODE = [200, 301, 400, 401, 404, 505]
SUPPORTED_VERSION = ["1.0"]
USING_VERSION = "1.0"
HEAD_LENGTH = 100
METHOD_DICT = {
    "GET": "get",
    "DELETE": "delete",
    "HEAD": "test",
    "POST": "update",
    "PUT": "add",
}
STATUS_CODE_DICT = {
    "OK": 200,
    "Moved Permanently": 301,
    "Bad Request": 400,
    "Unauthorized": 401,
    "NotFound": 404,
    "NotSupported": 505,
}
'''
shttp.py (simlar-http) contains the following functions:
    - parsing like-http packet
    - calling the data handler
    - replying the results by sending like-http packet

The format of my like-http is as follows:

2. Response message
    __________________________________________        ---+
    |    [version]   |SPACE|[status code]|CRLF|          | Status line
    |________________|_____|_____________|____|       ---+
    |       host          |SPACE|[value]|CRLF |          |
    |_____________________|_____|_______|___ _|          |
    |       Date          |SPACE|[value]|                | Header line
    |_____________________|_____|_______|                | 
    |   Content-Length    |SPACE|[VALUE]|                |
    |_____________________|_____|_______|              ---+
    |CRLF|                                               | Blank line
    |____|___________________________________         ---+
    |               Entity body              |           | request data
    |________________________________________|        ---+

    - status code
        - 200 OK                Request succeeded and the information is returned in the response
        - 301 Moved Permanently Requested object has been permanently moved
        - 400 Bad Request       A generic error code indicating that the request could not be understood by the server.
        - 401 Unauthorized      Does not have permission
        - 404 Not Found         The requested document does not exist on this server       
        - 505 Not Supported     The requested SHTTP protocol version is not supported by the server

'''

def response_message(version="1.0", status_code=200, host="127.0.0.1", content=""):
    date = str(datetime.datetime.now())
    head = "{0} {1}\nHost {2}\nDate {3}\nContent-Length {4}\n".format(
        version, status_code, host, date, len(content))
    head += (HEAD_LENGTH - 1 - len(head)) * ' ' + '\n'
    mess = head + content
    return mess


def check_header(head_dict):
    status_code = 200
    if head_dict["version"] not in SUPPORTED_VERSION:
        status_code = 505
    if head_dict["method"] not in METHOD_DICT:
        status_code = 400
    return status_code

def request_parsing(mess):
    print("parsing...")

    head = bytes.decode(mess[:HEAD_LENGTH])
    head_dict = {}
    head_lines = head.split('\n')

    head_dict["method"], head_dict["version"] = head_lines[0].split(' ')
    for line in head_lines[1:-2]:
        key, value = line.split(' ', 1)
        head_dict[key] = value
    print(head_dict)

    status_code = check_header(head_dict)

    item_info = content_parsing(mess[HEAD_LENGTH:], int(head_dict["Content-Length"]))
    return status_code, METHOD_DICT[head_dict["method"]], item_info


def content_parsing(content, decode_len):
    head = bytes.decode(content[:decode_len])
    item_info = {}
    items = head.split('\n')
    for item in items[:-1]:
        key, value = item.split(' ', 1)
        item_info[key] = value
    if "photo" in item_info:
        item_info["photo"] = content[decode_len:]

    return item_info