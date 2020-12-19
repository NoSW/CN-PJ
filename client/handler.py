from shttp import *
import socket

SERVER_ADDR = ('127.0.0.1', 8998)
BUFFSIZE = 1024*1024
DEFAULT_ITEM = {
    'id': None,
    'name': "No name",
    'val_photo': '2',
    'photo': None
}
METHOD_DICT = {
    "get": "GET",
    "delete": "DELETE",
    "test": "HEAD",
    "update": "POST",
    "add": "PUT",
}

def generate_content(item_info):
    content = ""
    for key in item_info.keys():
        content += key + ' ' + item_info[key] + '\n'
    return content

# The function (for ui.py) to send request to  server
def handler(instr, item_info):
    content  = generate_content(item_info)
    
    print("content: ", content)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(SERVER_ADDR)
        print("Successfully connected to server {}".format(SERVER_ADDR))
        mess = request_message(method=METHOD_DICT[instr], content=content)
        print("mess: \n", mess)
        s.sendall(mess.encode(DEFAULT_ENCODING))
        recv_data = s.recv(BUFFSIZE)
        return response_parsing(recv_data)
