import tkinter as tk
from tkinter import PhotoImage

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.geometry("400x300+550+270")
        center_window(self.root)

        self.root.resizable(False, False)

        # Load your image as a PhotoImage
        self.bg_image = PhotoImage(file="D:\\PartsManager\\Photos\\PORSCHE_911_GT2RS.png")

        # Create a Canvas to display the background image
        self.canvas = tk.Canvas(self.root, width=400, height=300)
        self.canvas.pack()

        # Display the background image on the Canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)

        # Create and configure the transparent label
        self.hello_label = tk.Label(self.canvas, text="Bine ati venit!", font=("Italic", "16"))
        self.hello_label.configure(bg=self.canvas.cget("bg"))
        self.hello_label.place(x=90, y=50)  # Adjust the label's position as needed

        # Rest of your code...

if __name__ == "__main__":
    def center_window(root):
        # Function to center the window on the screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    app = LoginWindow()
    app.root.mainloop()