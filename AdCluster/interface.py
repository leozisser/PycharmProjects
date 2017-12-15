from tkinter import filedialog
from tkinter import *
# import pymytest


def simscore():
    global score


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

root = Tk()
root.title(u'Выберите файл и нижний порог схожести')
root.resizable(True, True)
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)
entry3 = Entry(borderwidth=2, width=2, command=simscore())
entry3.grid(row = 1, column=3)
mainloop()