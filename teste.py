import tkinter as tk

class PartsManager:

    def __init__(self):

        self.win = tk.Tk()
        self.win.title("PartsManager")

        self.win.geometry("745x500")

        # Widgets

        self.auto_details_button = tk.Button(self.win,
                                             text="Auto Details",
                                             command=self.AutoDetails)
        self.auto_details_button.place(x=10, y=10)

        self.open_tec_doc_button = tk.Button(self.win,
                                             text="TecDoc",
                                             command=self.open_tec_doc)
        self.open_tec_doc_button.place(x=120, y=10)

        # Place other widgets using x and y coordinates as needed

        self.win.mainloop()

    def AutoDetails(self):
        # Define the functionality for the Auto Details button here
        pass

    def open_tec_doc(self):
        # Define the functionality for the TecDoc button here
        pass

if __name__ == "__main__":
    app = PartsManager()