from shttp import *


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

# The function (for ui.py) to send request to  server
def handler(instr, item_info, connection):

    send_mess = request_message(method=METHOD_DICT[instr], item_info=item_info)
    print("Soon-to-be sent:\n", send_mess[:min(len(send_mess), 150)], "...")
    connection.sendall(send_mess)
    recv_data = connection.recv(BUFFSIZE)
    status_code, item_info = response_parsing(recv_data)

    return STATUS_CODE_DICT[status_code], item_info
