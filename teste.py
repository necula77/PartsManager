import tkinter as tk
from tkinter import ttk

class AutoPartsManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Parts Manager")

        self.label = ttk.Label(root, text="Auto Parts Manager", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.parts_list = tk.Listbox(root, height=10, width=50)
        self.parts_list.pack(padx=20, pady=5)

        self.add_button = ttk.Button(root, text="Add Part")
        self.add_button.pack(pady=5)

        self.edit_button = ttk.Button(root, text="Edit Part")
        self.edit_button.pack(pady=5)

        self.delete_button = ttk.Button(root, text="Delete Part")
        self.delete_button.pack(pady=5)

        self.quit_button = ttk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)

if __name__ == "__main__":
    # root = tk.Tk()
    # app = AutoPartsManagerApp(root)
    # root.mainloop()
    try:
        somecode()  # raises NameError
    except Exception as e:
        print('Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e)))