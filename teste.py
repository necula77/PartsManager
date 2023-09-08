from tkinter import *
import os

tk=Tk()
var=StringVar()
Entry(tk,textvariable=var).pack()

# load the text before startup
if os.path.isfile('save.txt'):
    with open('save.txt','r') as f:
        var.set(f.read())

mainloop()

# save the text after shutdown
with open('save.txt','w') as f:
    f.write(var.get())