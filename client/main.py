import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from handler import handler
import socket

IMG_SIZE = (80, 80)

window = tk.Tk()
window.title("Student Information Management System")
window.geometry('600x1500')

# get Method
tk_method = tk.StringVar()
tk.Label(window, bg=None, width=40, text='').pack()
tk.Label(window, bg='yellow', width=20, text='What will you do ?').pack()
tk.Radiobutton(window, text='get a student\'s infomation', variable=tk_method, value="get", command=None).pack()
tk.Radiobutton(window, text='add a new student', variable=tk_method, value="add", command=None).pack()
tk.Radiobutton(window, text='delete a student', variable=tk_method, value="delete", command=None).pack()
tk.Radiobutton(window, text='update a student\'s infomation', variable=tk_method, value="update", command=None).pack()
# get Info
tk_id = tk.StringVar()
tk_name = tk.StringVar()
tk.Label(window, bg=None, width=20, text='').pack()
tk.Label(window, bg='yellow', width=20, text='Input id').pack()
tk.Entry(window, show=None, font=('Arial', 14), textvariable=tk_id).pack()
tk.Label(window, bg=None, width=20, text='').pack()
tk.Label(window, bg='yellow', width=20, text='Input name').pack()
tk.Entry(window, show=None, font=('Arial', 14), textvariable=tk_name).pack()

# get File
file_path = []
get_img = []
def add_file():
    file_path.clear()
    get_img.clear()

    tk.Label(window, bg='orange', width=20, text="id:\t{}\nname:\t{}".format(
        tk_id.get(), tk_name.get())).place(x = 300, y =450, anchor = "center")
    tk.Label(window, bg=None, width=20, text='').place(x = 300, y =480, anchor = "center")
    f = filedialog.askopenfilename()
    file_path.append(f)
    tk.Label(window, bg=None, width=100, text=file_path[-1]).place(x = 300, y =400, anchor = "center" )
    img = Image.open(file_path[-1])
    img.thumbnail((200, 200))
    img = ImageTk.PhotoImage(img)
    get_img.append(img)
    tk.Label(window, image=get_img[-1]).place(x=200, y=500)

tk.Label(window, bg=None, width=20, text='').pack()
tk.Label(window, bg='yellow', width=20, text='Upload the photo').pack()
tk.Button(window, text='upload', font=('Arial', 12), width=10, height=1, command=add_file).pack()
tk.Label(window, bg=None, width=20, text='').pack()

def generate_info_dict():

    instr = tk_method.get()
    if len(tk_id.get()) == 0:
        return None
    ret = {
        "id": tk_id.get(),
    }
    if len(tk_name.get()) != 0:
        ret["name"] = tk_name.get()
    else:
        if instr == "add":
            return None

    if len(file_path) != 0 and \
        (instr == "add" or instr == "update"):
        ret["val_photo"] = "1"
        with open(file_path[-1], 'rb') as f:
            ret['photo'] = f.read()
    else:
        ret["val_photo"] = "0"
        if instr == "add":
            return None

    return ret


def run():
    get_img.clear()
    instr = tk_method.get()
    if len(instr) == 0:
        print(tk.messagebox.showerror(title='ERROR',message='Please select an option!'))
        return
    item_info = generate_info_dict()
    if item_info == None:
        print(tk.messagebox.showerror(title='ERROR',message='No id or name or photo!'))
        return
    sc, item_info = handler(instr, item_info, s)
    if sc != "OK":
        print(tk.messagebox.showerror(title='ERROR',message='Filed! '+ sc))
    else:
        print(tk.messagebox.showinfo(title='INFO',message='Finished!'))
        file_path.clear()
    if len(item_info) != 0 and instr == "get":
        tk.Label(window, bg='orange', width=20, text="id:\t{}\nname:\t{}".format(
            item_info["id"], item_info["name"])).place(x = 300, y =450, anchor = "center")
        tk.Label(window, bg=None, width=20, text='').place(x = 300, y =480, anchor = "center")
        

        with open('tmp.jpg', "wb") as f:
            f.write(item_info["photo"])
        
        with Image.open('tmp.jpg') as img:
            # img = Image.frombytes(mode="RGBA", size=(60, 60), data=f.read(),decoder_name="raw")
            img.thumbnail((200, 200))
            img.save('a.jpg')
            img = ImageTk.PhotoImage(img)
            get_img.append(img)
        if len(get_img) != 0:
            tk.Label(window, image=get_img[-1]).place(x=200, y=500)
    
# Run
tk.Button(window, text='Run', font=('Arial', 12), width=10, height=1, command=run).place(x=400, y = 400)

SERVER_ADDR = ('127.0.0.1', 8998)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDR)
print("Successfully connected to server {}".format(SERVER_ADDR))


window.mainloop()