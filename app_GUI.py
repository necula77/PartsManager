import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import messagebox
import pandas as pd
import openpyxl
import DB_actions
import create_db
import login_sequence
import login_sequence as ls
from login_sequence import config
import logging
from PIL import Image, ImageTk
import json
import csv
import datetime
import os

USERNAME = ""

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                    datefmt="%d-%b-%Y %H:%M:%S",
                    handlers=[
                        logging.FileHandler("app.log"),  # apare intr un fisier
                        logging.StreamHandler()  # apare in consola ca un print
                    ]
                    )
def center_window(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def validate_input(p, max_char: int):
    """
    checks if the input provided by the user is correct
    :param p:
    :param max_char:
    :return:
    """

    if int(len(p)) <= int(max_char):
        return True
    else:
        return False


def run_app():
    """
    this function runs the app
    :return:
    """

    with open("app_config.json", 'r') as f:
        config_data = json.load(f)

    if config_data["first_app_open"] == "True":
        create_db.create_data_base()
        config_data["first_app_open"] = "False"
        with open("app_config.json", 'w') as f:
            json.dump(config_data, f, indent=4)

    LoginWindow()

    data = {}
    with open("AutoDetails.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)


class LoginWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.geometry("400x300+550+270")
        center_window(self.root)

        self.root.resizable(False, False)

        self.img = (Image.open("D:\\PartsManager\\Photos\\PORSCHE_911_GT2RS.png"))
        self.resized_image = self.img.resize((400,300))
        self.bg = ImageTk.PhotoImage(self.resized_image)
        # self.bg = PhotoImage(file="D:\\PartsManager\\Photos\\PORSCHE_911_GT2RS.png")
        self.image_label = tk.Label(self.root, image=self.bg)
        self.image_label.place(x=0, y=0)

        self.frame = tk.Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)

        # Buttons
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", "14"), command=self.login_btn_cmd)
        self.login_button.grid(row=5, column=1, pady=20)
        self.login_button.bind('<Return>', self.login_btn_cmd)

        # widgets declaration
        self.hello_label = tk.Label(self.root, text="Bine ati venit!", font=("Italic", "16"))
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", "14"))
        self.username_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
        self.username_entry.bind('<Return>', self.login_btn_cmd)
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", "14"))
        self.password_entry = tk.Entry(self.root, width=15, font=("Arial", "14"), show="*")
        self.password_entry.bind('<Return>', self.login_btn_cmd)

        # widgets rendering
        self.hello_label.grid(row=0, column=1, padx=90)
        self.username_label.grid(row=1, column=1, pady=10)
        self.username_entry.grid(row=2, column=1, pady=5)
        self.password_label.grid(row=3, column=1, pady=10)
        self.password_entry.grid(row=4, column=1, pady=5)

        self.root.mainloop()

    def login_btn_cmd(self, event=None):
        global USERNAME

        # authorization_level = ls.login_func(username=self.username_entry.get(), password=self.password_entry.get(), config=config)[0]
        # self.status = authorization_level[1]
        if self.username_entry.get() and self.password_entry.get():
            self.status, function, USERNAME = ls.login_func(username=self.username_entry.get(), password=self.password_entry.get(), config=config)
            if self.status is False:
                messagebox.showerror(title="Fail Authenticator", message="Username-ul sau parola sunt gresite.")
            else:
                self.root.destroy()
                PartsManager(function)


class PartsManager:

    global max_row
    global starting_x
    global starting_y

    next_row = 3
    max_row = 0
    starting_x = 5
    starting_y = 130

    def __init__(self, function):

        self.win = tk.Tk()
        self.win.title("PartsManager")

        self.win.geometry("745x500")
        # CENTRARE PE MIJLOC A APLICATIEI
        center_window(self.win)

        # CA SA PORNEASCA IN FULL SCREEN
        # self.win.state("zoomed")

        # NU POATE FI MINIMIZATA SAU MAXIMIZATA APLICATIA
        self.win.resizable(False, False)

        # pt full screen
        # self.width = self.win.winfo_screenwidth()
        # self.height = self.win.winfo_screenheight()
        # self.win.geometry("%dx%d" % (self.width, self.height))

        self.frame = tk.Frame(self.win)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.columnconfigure(5, weight=1)
        self.frame.columnconfigure(6, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)

        # Table

        self.entry_widgets = []

        self.add_table_row()

        # Buttons declaration

        self.auto_details_button = tk.Button(self.win,
                                             text="Auto Details",
                                             command=AutoDetails)

        self.auto_details_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.open_tec_doc_button = tk.Button(self.win,
                                             text="TecDoc",
                                             command=self.open_tec_doc)

        self.open_tec_doc_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.recieve_shipment_button = tk.Button(self.win,
                                                 text="Recieve Shipment",
                                                 command=RecieveShipment)
        # self.recieve_shipment_button.grid(row=0, column=2, pady=20)
        self.recieve_shipment_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.add_part_to_db_button = tk.Button(self.win,
                                               text="Manage Parts",
                                               command=ManageParts)
        # self.add_part_to_db_button.grid(row=0, column=3, pady=20)
        self.add_part_to_db_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.clear_table_button = tk.Button(self.win,
                                            text="Reset table",
                                            command=self.clear_table)
        # self.clear_table_button.grid(row=0, column=4, pady=20)
        self.clear_table_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.add_table_row_button = tk.Button(self.win,
                                              text="Add row",
                                              command=self.add_table_row)
        # self.add_table_row_button.grid(row=2, column=6, pady=40, sticky="ne")
        self.add_table_row_button.configure(borderwidth=1, font='Calibri 12 bold')

        if function == 'Admin':
            self.admin_panel_button = tk.Button(self.win,
                                                text="Admin Panel",
                                                command=AdminWindow)

            self.admin_panel_button.configure(borderwidth=1, font='Calibri 12 bold')
            self.admin_panel_button.place(x=430, y=30)

        self.save_and_open_button = tk.Button(self.win,
                                      text="Save and open \n in Excel",
                                      command=self.print_parts)
        self.save_and_open_button.configure(borderwidth=1, font='Calibri 12 bold')

        # Buttons rendering

        # self.auto_details_button.place(x=10, y=30)
        # self.open_tec_doc_button.place(x=280, y=30)
        # self.recieve_shipment_button.place(x=125, y=30)
        # self.add_part_to_db_button.place(x=360, y=30)
        # self.clear_table_button.place(x=490, y=30)
        # self.add_table_row_button.place(x=630, y=115)

        self.auto_details_button.place(x=620, y=170)
        self.open_tec_doc_button.place(x=630, y=225)
        self.recieve_shipment_button.place(x=600, y=280)
        self.add_part_to_db_button.place(x=615, y=335)
        self.clear_table_button.place(x=620, y=60)
        self.add_table_row_button.place(x=630, y=115)
        self.save_and_open_button.place(x=610, y=385)

        # widgets declaration

        self.conn_user_label = tk.Label(self.win, text="Connected user:", font=("Source Code Pro", "14"))
        self.username_label = tk.Label(self.win, text=USERNAME, font=("Source Code Pro", "14"), fg="#00FF00")
        self.part_name_label = tk.Label(self.win, text="Part Name", font=("Source Code Pro", "14"))
        self.part_number_label = tk.Label(self.win, text="Part Number", font=("Source Code Pro", "14"))
        self.stock_label = tk.Label(self.win, text="Stock", font=("Source Code Pro", "14"))
        self.price_label = tk.Label(self.win, text="Price", font=("Source Code Pro", "14"))
        self.location_in_warehouse_label = tk.Label(self.win, text="Location", font=("Source Code Pro", "14"))

        # self._entry = tk.Entry(self.win, width=15, font=("Arial", "14"))

        # widgets rendering

        self.conn_user_label.place(x=75, y=30)
        self.username_label.place(x=220, y=30)
        self.part_name_label.place(x=135, y=90)
        self.part_number_label.place(x=5, y=90)
        self.stock_label.place(x=270, y=90)
        self.price_label.place(x=390, y=90)
        self.location_in_warehouse_label.place(x=495, y=90)

        # self.part_number_label.grid(row=2, column=0, pady=10)
        # self.part_name_label.grid(row=2, column=1, pady=10)
        # self.stock_label.grid(row=2, column=2, pady=10)
        # self.price_label.grid(row=2, column=3, pady=10)
        # self.location_in_warehouse_label.grid(row=2, column=4, pady=10)
        # self._entry.grid(row=, column=, pady=5)

        self.win.mainloop()
        self.status = False

    def add_table_row(self):
        global max_row
        global starting_x
        global starting_y

        starting_x = 5

        if max_row < 15:
            row_widgets = []

            for i in range(5):

                new_row = tk.Entry(self.win, width=16, fg="black", font=('Arial', 10, 'bold'))
                # new_row.grid(row=self.next_row, column=i)
                new_row.place(x=starting_x, y=starting_y)
                starting_x += 117

                if i == 0:
                    new_row.bind('<Return>', self.fill_table_entries)

                row_widgets.append(new_row)

            starting_y += 20
            self.entry_widgets.append(row_widgets)
            self.next_row += 1
            max_row += 1
        else:
            tk.messagebox.showinfo(title="Maximum rows",
                                   message="Maximum number of rows has been reached, please create a new app.")

    def clear_table(self):
        global max_row
        global starting_x
        global starting_y

        starting_x = 5
        starting_y = 130

        for row_widgets in self.entry_widgets:
            for entry in row_widgets:
                entry.destroy()
        self.entry_widgets.clear()
        max_row = 0
        self.add_table_row()

    def fill_table_entries(self, event=None):  # Accept the event argument, but it's not used
        for row_widgets in self.entry_widgets:
            part_number_entry = row_widgets[0].get()  # Assuming the first entry is for part numbers
            if part_number_entry:
                data = DB_actions.recieve_info_abt_part(part_number=part_number_entry)
                if data:
                    # Assuming data is a dictionary with keys for part name, stock, price, and location
                    part_name, stock, price, location = data[0], data[1], data[2], data[3]
                    row_widgets[1].delete(0, tk.END)  # Clear the existing entry
                    row_widgets[1].insert(0, part_name)
                    row_widgets[2].delete(0, tk.END)
                    row_widgets[2].insert(0, stock)
                    row_widgets[3].delete(0, tk.END)
                    row_widgets[3].insert(0, price)
                    row_widgets[4].delete(0, tk.END)
                    row_widgets[4].insert(0, location)
                else:
                    # Handle the case where data is not found for the given part number
                    messagebox.showerror("Error", f"Data not found for part number: {part_number_entry}")
            else:
                # Handle the case where the part number entry is empty
                messagebox.showerror("Error", "Part number cannot be empty")

    def open_tec_doc(self):
        webbrowser.open('https://web.tecalliance.net/tecdocsw/ro/login')

    def print_parts(self):
        """
        This function takes the parts information from the app's table and transforms them into an Excel file (xlsx).
        """
        current_time = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S")

        try:
            with open("AutoDetails.json", "r") as f:
                json_data = f.read()
                data = json.loads(json_data)
            vin = data["VIN"]
            km = data["KM"]

            output_directory = "D://PartsManager//temp_files"
            excel_output_directory = "D:\\PartsManager\\xlsx_files"

            csv_file = os.path.join(output_directory, f"parts_data_{vin}_{km}_{current_time}.csv")
            excel_file = os.path.join(excel_output_directory,
                                      f"parts_data_{vin}_{km}km_{current_time}.xlsx")

            data_to_write = [["Part Number", "Part Name", "Stock", "Price", "Location"]]

            for row_widgets in self.entry_widgets:
                part_number = row_widgets[0].get()
                part_name = row_widgets[1].get()
                stock = row_widgets[2].get()
                price = row_widgets[3].get()
                location = row_widgets[4].get()

                data_to_write.append([part_number, part_name, stock, price, location])

        except KeyError as e:

            tk.messagebox.showerror(title="Error",
                                    message="Please fill out information about car in AutoDetails window.")

        except Exception as e:
            print(e)

        try:
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data_to_write)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data to {csv_file}: {str(e)}")

        try:

            csv_read = pd.read_csv(csv_file)

            workbook = openpyxl.Workbook()
            worksheet = workbook.active

            data_to_write_excel = [list(csv_read.columns)] + csv_read.values.tolist()

            for row in data_to_write_excel:
                worksheet.append(row)

            workbook.save(excel_file)

            os.remove(csv_file)

            os.startfile(excel_file)

            for row_widgets in self.entry_widgets:
                part_number = row_widgets[0].get()
                DB_actions.remove_stock(part_number=part_number,stock_to_remove=1)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data to {excel_file}: {str(e)}")


class AdminWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin panel")
        self.root.geometry("250x300")
        center_window(self.root)
        self.root.resizable(False, False)


        # Buttons declarations

        self.register_user_button = tk.Button(self.root,
                                              text="Regiser user",
                                              command=self.register_user_window)
        self.register_user_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.delete_user_button = tk.Button(self.root,
                                            text="Delete user",
                                            command=self.delete_user)
        self.delete_user_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.update_user_login_info_button = tk.Button(self.root,
                                                       text="Update user login info",
                                                       command=self.update_user_login_info)
        self.update_user_login_info_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.delete_car_button = tk.Button(self.root,
                                           text="Delete car information",
                                           command=self.delete_car_information)
        self.delete_car_button.configure(borderwidth=1, font='Calibri 12 bold')

        # Buttons rendering

        self.register_user_button.place(x=80, y=50)
        self.delete_user_button.place(x=83, y=100)
        self.update_user_login_info_button.place(x=45, y=150)
        self.delete_car_button.place(x=43, y=200)

        # Widgets declarations

        # Widgets rendering

        self.root.mainloop()

    def register_user_window(self):
        root = tk.Tk()
        root.title("Register user")
        root.geometry("400x300")
        center_window(root)
        root.resizable(False, False)


        # Buttons declarations

        register_button = tk.Button(root,
                                    text="Register user",
                                    command=self.register_user_function)
        register_button.configure(borderwidth=1, font='Calibri 12 bold')

        clear_button = tk.Button(root,
                                text="Clear",
                                 command=self.clear_btn_func)
        clear_button.configure(borderwidth=1, font='Calibri 12 bold')

        # Buttons rendering

        register_button.place(x=140, y=225)
        clear_button.place(x=25, y=225)

        # Widgets declarations

        first_name_label = tk.Label(root, text="First name:", font=("Arial", "14"))
        last_name_label = tk.Label(root, text="Last name:", font=("Arial", "14"))
        username_label = tk.Label(root, text="Username:", font=("Arial", "14"))
        password_label = tk.Label(root, text="Password:", font=("Arial", "14"))
        function_label = tk.Label(root, text="Function:", font=("Arial", "14"))

        self.first_name_entry = tk.Entry(root, width=15, font=("Arial", "14"))
        self.last_name_entry = tk.Entry(root, width=15, font=("Arial", "14"))
        self.username_entry = tk.Entry(root, width=15, font=("Arial", "14"))
        self.password_entry = tk.Entry(root, width=15, font=("Arial", "14"))
        self.function_entry = tk.Entry(root, width=15, font=("Arial", "14"))

        # Widgets rendering

        first_name_label.place(x=5, y=10)
        last_name_label.place(x=5, y=50)
        username_label.place(x=5, y=90)
        password_label.place(x=7, y=130)
        function_label.place(x=10, y=170)

        self.first_name_entry.place(x=110, y=12)
        self.last_name_entry.place(x=110, y=52)
        self.username_entry.place(x=110, y=92)
        self.password_entry.place(x=110, y=132)
        self.function_entry.place(x=110, y=172)

        root.mainloop()

    def register_user_function(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        function = self.function_entry.get()

        if first_name == '' or last_name == '' or username == '' or password == '' or function == '':
            tk.messagebox.showerror(title="Error", message="All fields must be completed!")
            self.root.destroy()

        status = login_sequence.signup_func(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            function=function,
                                            logged_user=USERNAME)

    def clear_btn_func(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.function_entry.delete(0, 'end')

    def delete_user(self):
        self.root = tk.Tk()
        self.root.title("Delete user")
        self.root.geometry("380x150")
        center_window(self.root)
        self.root.resizable(False, False)
        # Buttons declarations

        delete_button = tk.Button(self.root,
                                  text="Delete",
                                  command=self.delete_btn_func)
        delete_button.configure(borderwidth=1, font='Calibri 12 bold')

        # Buttons rendering

        delete_button.place(x=300, y=50)

        # Widgets declarations

        username_label = tk.Label(self.root, text="Username:", font=("Arial", "14"))
        first_name_label = tk.Label(self.root, text="First name:", font=("Arial", "14"))
        last_name_label = tk.Label(self.root, text="Last name:", font=("Arial", "14"))

        self.username_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
        self.first_name_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
        self.last_name_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        # Widgets rendering

        username_label.place(x=5, y=10)
        first_name_label.place(x=5, y=50)
        last_name_label.place(x=5, y=90)

        self.username_entry.place(x=110, y=12)
        self.first_name_entry.place(x=110, y=52)
        self.last_name_entry.place(x=110, y=92)

        self.root.mainloop()

    def delete_btn_func(self):

        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        question = tk.messagebox.askokcancel(title="Confirmation", message=f"Are you sure that you want to delete"
                                                                           f" '{username}' from the database?")

        if question is True:
            status = login_sequence.delete_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                logged_user=USERNAME)

        self.root.destroy()

    def update_user_login_info(self):
        self.win = tk.Tk()
        self.win.title("Insert username")
        self.win.geometry("300x100")
        center_window(self.win)
        self.win.resizable(False,False)

        username_label = tk.Label(self.win, text="Username:", font=("Arial", "14"))
        self.username_entry = tk.Entry(self.win, width=15, font=("Arial", "14"))

        username_label.place(x=5, y=20)
        self.username_entry.place(x=105, y=22)

        check_button = tk.Button(self.win,
                                 text="Check",
                                 command=self.check_btn_func)
        check_button.configure(borderwidth=1, font='Calibri 12 bold')

        check_button.place(x=150, y=55)

    def check_btn_func(self):
        username = self.username_entry.get()

        self.data = login_sequence.verify_if_user_exists(username=username)

        if self.data:
            self.win.destroy()

            self.root = tk.Tk()
            self.root.title("Update user information")
            self.root.geometry("400x300")
            center_window(self.root)
            self.root.resizable(False, False)

            # Buttons declarations

            update_button = tk.Button(self.root,
                                      text="Update",
                                      command=self.update_btn_func)
            update_button.configure(borderwidth=1, font='Calibri 12 bold')

            # Buttons rendering

            update_button.place(x=155, y=210)

            # Widgets declarations

            first_name_label = tk.Label(self.root, text="First name:", font=("Arial", "14"))
            last_name_label = tk.Label(self.root, text="Last name:", font=("Arial", "14"))
            username_label = tk.Label(self.root, text="Username:", font=("Arial", "14"))
            password_label = tk.Label(self.root, text="Password:", font=("Arial", "14"))
            function_label = tk.Label(self.root, text="Function:", font=("Arial", "14"))

            self.first_name_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
            self.last_name_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
            self.username_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
            self.password_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))
            self.function_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

            # Widgets rendering

            first_name_label.place(x=5, y=10)
            last_name_label.place(x=5, y=50)
            username_label.place(x=5, y=90)
            password_label.place(x=7, y=130)
            function_label.place(x=10, y=170)

            self.first_name_entry.place(x=110, y=12)
            self.last_name_entry.place(x=110, y=52)
            self.username_entry.place(x=110, y=92)
            self.password_entry.place(x=110, y=132)
            self.function_entry.place(x=110, y=172)

            self.root.mainloop()

    def update_btn_func(self):

        user_id = self.data[0]
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        function = self.function_entry.get()

        status = login_sequence.edit_user_info(user_id=user_id,
                                               first_name=first_name,
                                               last_name=last_name,
                                               new_username=username,
                                               password=password,
                                               function=function,
                                               logged_user=USERNAME)

        self.root.destroy()

    def delete_car_information(self):
        self.root = tk.Tk()
        self.root.title("Delete car information")
        self.root.geometry("350x100")
        center_window(self.root)
        self.root.resizable(False, False)

        # Buttons declarations

        delete_button = tk.Button(self.root,
                                  text="Delete",
                                  width=10,
                                  command=self.delete_car_info_btn)
        delete_button.configure(borderwidth=1, font='Calibri 10 bold')

        # Buttons rendering

        delete_button.place(x=250, y=52)

        # Widgets declarations

        vin_label = tk.Label(self.root, text="VIN:", font=("Arial", "14"))
        l_plate_label = tk.Label(self.root, text="License plate:", font=("Arial", "14"))

        self.vin_entry = tk.Entry(self.root, width=25, font=("Arial", "14"))
        self.l_plate_entry = tk.Entry(self.root, width=10, font=("Arial", "14"))

        # Widgets rendering

        vin_label.place(x=5, y=20)
        l_plate_label.place(x=5, y=50)

        self.vin_entry.place(x=50, y=22)
        self.l_plate_entry.place(x=130, y=52)

        self.root.mainloop()

    def delete_car_info_btn(self):

        vin = self.vin_entry.get()
        plate = self.l_plate_entry.get()

        question = tk.messagebox.askyesno(title="Are you sure?", message="Are you sure that you want to delete"
                                                                         "this car's info from the database?")

        if question is True:

            status = DB_actions.delete_car_info(vin=vin,
                                                license_plate=plate,
                                                logged_user=USERNAME)

            if status is True:
                tk.messagebox.showinfo(title="Succes", message="The car's info was deleted sucesfully!")
            else:
                tk.messagebox.showerror(title="Error", message="The car's info could not be deleted!")

            self.root.destroy()
        else:
            self.root.destroy()


class AutoDetails:

    def __init__(self):

        self.config = config
        self.root = tk.Tk()
        self.root.title("Auto Details")
        self.root.geometry("535x320+550+270")
        # self.root.wm_attributes("-topmost", True)

        center_window(self.root)
        # Buttons

        self.send_button = tk.Button(self.root, text="Send", font=("Arial", "14"), command=self.send_btn_cmd)
        self.send_button.grid(row=7, column=4, pady=20)

        self.retrieve_button = tk.Button(self.root, text="Retrieve data",
                                         font=("Arial", "14"),
                                         command=self.retrieve_btn_cmd)
        self.retrieve_button.grid(row=7, column=3, pady=20)
        self.retrieve_button.bind('<Return>', self.send_btn_cmd)

        self.back_button = tk.Button(self.root, text="Back", font=("Arial", "14"), command=self.root.destroy)
        self.back_button.grid(row=7, column=2, pady=20)

        # widgets declaration
        self.vin_label = tk.Label(self.root, text="VIN", font=("Arial", "14"))
        self.vin_entry = tk.Entry(self.root,
                                  validate="key",
                                  validatecommand=(self.root.register(validate_input), "%P", 17),
                                  width=15,
                                  font=("Arial", "14"))

        self.license_plate_label = tk.Label(self.root, text="License plate", font=("Arial", "14"))
        self.license_plate_entry = tk.Entry(self.root,
                                            validate="key",
                                            validatecommand=(self.root.register(validate_input), "%P", 10),
                                            width=15,
                                            font=("Arial", "14"))

        # self.data = self.retrieve_btn_cmd()

        self.engine_label = tk.Label(self.root, text="Engine", font=("Arial", "14"))
        self.engine_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.kw_label = tk.Label(self.root, text="KW", font=("Arial", "14"))
        self.kw_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.cc_label = tk.Label(self.root, text="CC", font=("Arial", "14"))
        self.cc_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.km_label = tk.Label(self.root, text="KM", font=("Arial", "14"))
        self.km_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.make_label = tk.Label(self.root, text="Make", font=("Arial", "14"))
        self.make_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.model_label = tk.Label(self.root, text="Model", font=("Arial", "14"))
        self.model_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.year_label = tk.Label(self.root, text="Year", font=("Arial", "14"))
        self.year_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.fuel_type_label = tk.Label(self.root, text="Fuel Type", font=("Arial", "14"))
        self.fuel_type_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        # widgets rendering
        self.vin_label.grid(row=2, column=1, pady=10)
        self.vin_entry.grid(row=2, column=2, pady=5)

        self.license_plate_label.grid(row=2, column=3, pady=10)
        self.license_plate_entry.grid(row=2, column=4, pady=5)

        self.engine_label.grid(row=3, column=1, pady=10)
        self.engine_entry.grid(row=3, column=2, pady=5)

        self.km_label.grid(row=3, column=3, pady=10)
        self.km_entry.grid(row=3, column=4, pady=5)

        self.kw_label.grid(row=4, column=1, pady=10)
        self.kw_entry.grid(row=4, column=2, pady=5)

        self.cc_label.grid(row=4, column=3, pady=10)
        self.cc_entry.grid(row=4, column=4, pady=5)

        self.make_label.grid(row=5, column=1, pady=10)
        self.make_entry.grid(row=5, column=2, pady=5)

        self.model_label.grid(row=5, column=3, pady=10)
        self.model_entry.grid(row=5, column=4, pady=5)

        self.year_label.grid(row=6, column=1, pady=10)
        self.year_entry.grid(row=6, column=2, pady=5)

        self.fuel_type_label.grid(row=6, column=3, pady=10)
        self.fuel_type_entry.grid(row=6, column=4, pady=5)

        self.fill_entries_from_json()

        self.root.mainloop()

    def save_data_to_json(self):

        data = {
            "VIN": self.vin_entry.get(),
            "License Plate": self.license_plate_entry.get(),
            "Engine": self.engine_entry.get(),
            "KM": self.km_entry.get(),
            "KW": self.kw_entry.get(),
            "CC": self.cc_entry.get(),
            "Make": self.make_entry.get(),
            "Model": self.model_entry.get(),
            "Year": self.year_entry.get(),
            "Fuel Type": self.fuel_type_entry.get()
        }

        file_path = "AutoDetails.json"

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def fill_entries_from_json(self):

        file_path = "AutoDetails.json"

        try:

            data = {}

            with open("AutoDetails.json", "r") as f:
                text = f.read()
                if text:
                    data = json.loads(text)

            self.vin_entry.delete(0, 'end')
            self.vin_entry.insert(0, data.get("VIN", ""))

            self.license_plate_entry.delete(0, 'end')
            self.license_plate_entry.insert(0, data.get("License Plate", ""))

            self.engine_entry.delete(0, 'end')
            self.engine_entry.insert(0, data.get("Engine", ""))

            self.km_entry.delete(0, 'end')
            self.km_entry.insert(0, data.get("KM", ""))

            self.kw_entry.delete(0, 'end')
            self.kw_entry.insert(0, data.get("KW", ""))

            self.cc_entry.delete(0, 'end')
            self.cc_entry.insert(0, data.get("CC", ""))

            self.make_entry.delete(0, 'end')
            self.make_entry.insert(0, data.get("Make", ""))

            self.model_entry.delete(0, 'end')
            self.model_entry.insert(0, data.get("Model", ""))

            self.year_entry.delete(0, 'end')
            self.year_entry.insert(0, data.get("Year", ""))

            self.fuel_type_entry.delete(0, 'end')
            self.fuel_type_entry.insert(0, data.get("Fuel Type", ""))

        except FileNotFoundError:
            messagebox.showerror(title="Error", message="Fisierul Json nu a fost gasit!")

    def send_btn_cmd(self):
        # functie care trimite datele auto spre baza de date in cazul in care nu sunt deja in ea

        vin = self.vin_entry.get()
        plate = self.license_plate_entry.get()
        engine = self.engine_entry.get()
        km = self.km_entry.get()
        kw = self.kw_entry.get()
        cc = self.cc_entry.get()
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = self.year_entry.get()
        fuel_type = self.fuel_type_entry.get()

        check_for_car = DB_actions.check_for_car(vin=vin, license_plate=plate)

        if check_for_car is True:
            sql_query = f"""UPDATE "Auto_Details"."REGISTERED_CARS"
                            SET "Engine" = '{self.engine_entry.get()}',
                                "KW" = '{self.kw_entry.get()}',
                                "CMC" = '{self.cc_entry.get()}',
                                "Fuel_Type" = '{self.fuel_type_entry.get()}',
                                "KM" = '{self.km_entry.get()}'
                            WHERE "VIN" = '{self.vin_entry.get()}';"""
        else:
            sql_query = f"""INSERT INTO "Auto_Details"."REGISTERED_CARS" 
                            ("VIN", "License Plate", "Manufacturer", "Model",
                             "Year", "Engine", "KW", "CMC", "Fuel_Type", "KM")
                            VALUES ('{vin}', '{plate}', '{make}', '{model}',
                            {year}, '{engine}', {kw}, {cc}, '{fuel_type}', {km});"""

        status = DB_actions.insert_in_db(config=config, sql_query=sql_query,
                                         logged_user=USERNAME, license_plate=self.license_plate_entry.get(),
                                         vin=self.vin_entry.get())

        self.save_data_to_json()

        if status is True:
            messagebox.showinfo(title="Message", message="Datele au fost introduse cu succes.")

    def retrieve_btn_cmd(self):

        with open("AutoDetails.json", "r") as f:
            text = f.read()
            if text:
                data = json.loads(text)

                if data:
                    if self.license_plate_entry.get() != data["License Plate"] and self.license_plate_entry.get():
                        self.delete_data_from_entrys(delete_license=False)
                    if self.vin_entry.get() != data["VIN"] and self.vin_entry.get():
                        self.delete_data_from_entrys(delete_vin=False)

        with open("AutoDetails.json", 'w') as f:
            f.truncate()

        data_dict = {
            "VIN": "",
            "License Plate": "",
            "Manufacturer": "",
            "Model": "",
            "Year": "",
            "Engine": "",
            "KW": "",
            "CMC": "",
            "Fuel_Type": "",
            "KM": ""
        }
        vin = self.vin_entry.get()
        license = self.license_plate_entry.get()
        data = DB_actions.recieve_from_db(vin=vin, license_plate=license)

        self.delete_data_from_entrys()

        # now inserting data into entrys
        self.vin_entry.insert(0, data['VIN'])
        self.license_plate_entry.insert(0, data['License Plate'])
        self.engine_entry.insert(0, data['Engine'])
        self.km_entry.insert(0, data['KM'])
        self.kw_entry.insert(0, data['KW'])
        self.cc_entry.insert(0, data['CMC'])
        self.make_entry.insert(0, data['Manufacturer'])
        self.model_entry.insert(0, data['Model'])
        self.year_entry.insert(0, data['Year'])
        self.fuel_type_entry.insert(0, data['Fuel_Type'])

        self.save_data_to_json()

        return data

    def delete_data_from_entrys(self, delete_vin=True, delete_license=True):
        # deleting data from entrys
        if delete_vin is True:
            self.vin_entry.delete(0, 'end')
        if delete_license is True:
            self.license_plate_entry.delete(0, 'end')
        self.engine_entry.delete(0, 'end')
        self.km_entry.delete(0, 'end')
        self.kw_entry.delete(0, 'end')
        self.cc_entry.delete(0, 'end')
        self.make_entry.delete(0, 'end')
        self.model_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.fuel_type_entry.delete(0, 'end')

    def get_vin(self):
        return self.vin_entry.get()


class ManageParts:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manage Parts")
        self.root.geometry("480x260")
        center_window(self.root)

        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=2)
        self.root.columnconfigure(4, weight=2)

        # Buttons

        self.add_part_button = tk.Button(self.root, text="Add part", font=("Arial", "14"), command=self.add_part_btn_cmd)
        self.add_part_button.configure(borderwidth=1, font='Calibri 11 bold')
        # self.send_button.grid(row=7, column=4, pady=20)
        self.add_part_button.place(x=399, y=58)

        # self.retrieve_data_button = tk.Button(self.root, text="Retrieve data", font=("Arial", "14"))
        # self.retrieve_data_button.configure(borderwidth=1, font='Calibri 14 bold')
        # # self.retrieve_data_button.grid(row=7, column=3, pady=20)
        # self.retrieve_data_button.place(x=158, y=250)

        # self.clear_button = tk.Button(self.root, text="Clear", font=("Arial", "14"))
        # self.clear_button.configure(borderwidth=1, font='Calibri 14 bold')
        # # self.clear_button.grid(row=7, column=2, pady=20)
        # self.clear_button.place(x=45, y=250)

        self.remove_button = tk.Button(self.root, text="Remove", font=("Arial", "14"), command=self.remove_btn_cmd)
        self.remove_button.configure(borderwidth=1, font='Calibri 11 bold')
        # self.remove_button.grid(row=7, column=1, pady=20)
        self.remove_button.place(x=400, y=10)

        # Widgets declaration

        self.part_number_label = tk.Label(self.root, text="Part number", font=("Arial", "14"))
        self.part_number_entry = tk.Entry(self.root, width=20, font=("Arial", "14"))

        self.part_name_label = tk.Label(self.root, text="Part name", font=("Arial", "14"))
        self.part_name_entry = tk.Entry(self.root, width=20, font=("Arial", "14"))

        self.stock_label = tk.Label(self.root, text="Stock", font=("Arial", "14"))
        self.stock_entry = tk.Entry(self.root, width=20, font=("Arial", "14"))

        self.location_label = tk.Label(self.root, text="Location", font=("Arial", "14"))
        self.location_entry = tk.Entry(self.root, width=20, font=("Arial", "14"))

        self.price_label = tk.Label(self.root, text="Price", font=("Arial", "14"))
        self.price_entry = tk.Entry(self.root, width=20, font=("Arial", "14"))

        # Widgets rendering

        self.part_number_label.grid(row=2, column=1, pady=10)
        self.part_number_entry.grid(row=2, column=2, pady=5)

        self.part_name_label.grid(row=3, column=1, pady=10)
        self.part_name_entry.grid(row=3, column=2, pady=5)

        self.stock_label.grid(row=4, column=1, pady=10)
        self.stock_entry.grid(row=4, column=2, pady=5)

        self.location_label.grid(row=5, column=1, pady=10)
        self.location_entry.grid(row=5, column=2, pady=5)

        self.price_label.grid(row=6, column=1, pady=10)
        self.price_entry.grid(row=6, column=2, pady=5)

        self.root.mainloop()

    def position_empty_label(self, row, column):
        # label to position the button better
        self.empty_label = tk.Label(self.root, text="      ", font=("Source Code Pro", "14"))
        self.empty_label.grid(row=row, column=column, pady=10)

    def add_part_btn_cmd(self):

        part_number = self.part_number_entry.get()
        part_name = self.part_name_entry.get()
        stock = self.stock_entry.get()
        location = self.location_entry.get()
        price = self.price_entry.get()

        status = DB_actions.register_part(part_number=part_number,
                                          part_name=part_name,
                                          stock=stock,
                                          location=location,
                                          price=price,
                                          logged_user=USERNAME)

        self.root.destroy()

    def remove_btn_cmd(self):

        part_number = self.part_number_entry.get()

        status = DB_actions.remove_part(part_number=part_number,
                                        logged_user=USERNAME)

        self.root.destroy()


class RecieveShipment:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Recieve Shipment")
        self.root.geometry("310x180")
        center_window(self.root)

        # Buttons

        self.recieve_button = tk.Button(self.root, text="Recieve", font=("Arial", "14"), command=self.recieve_btn_cmd)
        self.recieve_button.grid(row=3, column=2, pady=20)

        self.clear_button = tk.Button(self.root, text="Clear", font=("Arial", "14"), command=self.clear_btn_cmd)
        self.clear_button.grid(row=3, column=1, pady=20)

        # Widgets declaration

        self.part_number_label = tk.Label(self.root, text="Part number", font=("Arial", "14"))
        self.part_number_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        self.stock_label = tk.Label(self.root, text="Stock recieved", font=("Arial", "14"))
        self.stock_entry = tk.Entry(self.root, width=15, font=("Arial", "14"))

        # Widgets rendering

        self.part_number_label.grid(row=1, column=1, pady=10)
        self.part_number_entry.grid(row=1, column=2, pady=5)

        self.stock_label.grid(row=2, column=1, pady=10)
        self.stock_entry.grid(row=2, column=2, pady=5)

        self.root.mainloop()

    def recieve_btn_cmd(self):

        part_number = self.part_number_entry.get()
        stock_to_add = self.stock_entry.get()

        status = DB_actions.recieve_shipment(part_number=part_number,
                                             stock_to_add=stock_to_add,
                                             logged_user=USERNAME)

        if status is True:
            return messagebox.showinfo(title="Message",
                                       message=f"Stock-ul pentru piesa {part_number} a fost modificat cu succes."),\
                   self.root.destroy()
        else:
            return messagebox.showerror(title="Error",
                                        message=f"Stock-ul nu poate fi modificat, va rugam sa verificati datele introduse.")

    def clear_btn_cmd(self):
        self.part_number_entry.delete(0, 'end')
        self.stock_entry.delete(0, 'end')


if __name__ == "__main__":

    run_app()
