import tkinter as tk 
from handler import handler

def ui():
    item_info = {
        "id": "00006",
        "name": "Lee",
        "val_photo": "0",
    }
    print(handler("get", item_info))
