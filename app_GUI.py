import tkinter as tk
from tkinter import *
from tkinter import messagebox
import login_sequence as ls
from login_sequence import config
import psycopg2 as ps
import logging
import DB_actions
import webbrowser
import cv2
from PIL import Image, ImageTk
import json

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


def validate_input(P, max_char: int):
    if int(len(P)) <= int(max_char):
        return True
    else:
        return False


class PartsManager():

    def __init__(self):

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
        self.frame.columnconfigure(1, weight=2)
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

        self.table_row = self.create_table(1, 5, start_row=3)

        # Buttons

        self.auto_details_button = tk.Button(self.win, text="Auto Details", font=("Arial", "14"), command=AutoDetails)
        self.auto_details_button.grid(row=0, column=0, pady=20)
        self.auto_details_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.open_tec_doc_button = tk.Button(self.win, text="TecDoc", font=("Arial", "14"), command=self.open_tec_doc)
        self.open_tec_doc_button.grid(row=0, column=1, pady=20)
        self.open_tec_doc_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.recieve_shipment_button = tk.Button(self.win, text="Recieve Shipment", font=("Arial", "14"))
        self.recieve_shipment_button.grid(row=0, column=2, pady=20)
        self.recieve_shipment_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.add_part_to_db_button = tk.Button(self.win,
                                               text="Manage Parts",
                                               font=("Arial", "14"),
                                               command=ManageParts)
        self.add_part_to_db_button.grid(row=0, column=3, pady=20)
        self.add_part_to_db_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.add_table_row_button = tk.Button(self.win,
                                              text="Add row",
                                              font=("Arial", "14"),
                                              command=lambda: self.add_table_row(self.table_row))

        self.position_empty_label(3, 5)

        self.add_table_row_button.grid(row=3, column=6, pady=40, sticky="e")
        self.add_table_row_button.configure(borderwidth=1, font='Calibri 12 bold')

        # widgets declaration

        self.part_name_label = tk.Label(self.win, text="Part Name", font=("Source Code Pro", "14"))
        self.part_number_label = tk.Label(self.win, text="Part Number", font=("Source Code Pro", "14"))
        self.stock_label = tk.Label(self.win, text="Stock", font=("Source Code Pro", "14"))
        self.price_label = tk.Label(self.win, text="Price", font=("Source Code Pro", "14"))
        self.location_in_warehouse_label = tk.Label(self.win, text="Location", font=("Source Code Pro", "14"))

        self._entry = tk.Entry(self.win, width=15, font=("Arial", "14"))

        # widgets rendering

        self.part_number_label.grid(row=2, column=0, pady=10)
        self.part_name_label.grid(row=2, column=1, pady=10)
        self.stock_label.grid(row=2, column=2, pady=10)
        self.price_label.grid(row=2, column=3, pady=10)
        self.location_in_warehouse_label.grid(row=2, column=4, pady=10)
        # self._entry.grid(row=, column=, pady=5)

        self.win.mainloop()
        self.status = False

    def position_empty_label(self, row, column):
        # label to position the button better
        self.empty_label = tk.Label(self.win, text="      ", font=("Source Code Pro", "14"))
        self.empty_label.grid(row=row, column=column, pady=10)

    def create_table(self, row, column, start_row=0):
        last_row = 0

        for i in range(row):
            last_row += 1
            for j in range(column):
                table = tk.Entry(self.win, width=10, fg="gray", font=('Arial', 16, 'bold'))
                table.grid(row=i + start_row, column=j)

        return last_row

    def add_table_row(self, actual_row):

        for j in range(5):
            table = tk.Entry(self.win, width=10, fg="gray", font=('Arial', 16, 'bold'))
            table.grid(row=actual_row, column=j)

    def open_tec_doc(self):
        webbrowser.open('https://web.tecalliance.net/tecdocsw/ro/login')


class ManageParts:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manage Parts")
        self.root.geometry("535x320+550+270")
        center_window(self.root)

        # Buttons

        self.send_button = tk.Button(self.root, text="Send", font=("Arial", "14"), command=self.send_btn_cmd)
        self.send_button.grid(row=7, column=3, pady=20)

        self.clear_button = tk.Button(self.root, text="Clear", font=("Arial", "14"))
        self.clear_button.grid(row=7, column=2, pady=20)

        self.remove_button = tk.Button(self.root, text="Remove", font=("Arial", "14"))
        self.remove_button.grid(row=7, column=1, pady=20)

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

    def send_btn_cmd(self):

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

        if status is True:
            return messagebox.showinfo(title="Message",
                                       message=f"Piesa {part_name} a fost introdusa cu succes."),\
                   self.root.destroy()
        else:
            return messagebox.showerror(title="Error",
                                        message=f"Piesa nu poate fi adaugata, va rugam sa verificati datele introduse.")


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
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

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

        sql_query = f"""UPDATE "Auto_Details"."REGISTERED_CARS"
                        SET "Engine" = '{self.engine_entry.get()}',
                            "KW" = '{self.kw_entry.get()}',
                            "CMC" = '{self.cc_entry.get()}',
                            "Fuel_Type" = '{self.fuel_type_entry.get()}',
                            "KM" = '{self.km_entry.get()}'
                        WHERE "VIN" = '{self.vin_entry.get()}';"""

        status = DB_actions.insert_in_db(config=config, sql_query=sql_query,
                                         logged_user=USERNAME, license_plate=self.license_plate_entry.get(),
                                         vin=self.vin_entry.get())

        self.save_data_to_json()

        if status is True:
            messagebox.showinfo(title="Message", message="Datele au fost introduse cu succes.")

    def retrieve_btn_cmd(self):

        json_data = {}
        with open("AutoDetails.json", 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

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

        # deleting data from entrys
        self.vin_entry.delete(0, 'end')
        self.license_plate_entry.delete(0, 'end')
        self.engine_entry.delete(0, 'end')
        self.km_entry.delete(0, 'end')
        self.kw_entry.delete(0, 'end')
        self.cc_entry.delete(0, 'end')
        self.make_entry.delete(0, 'end')
        self.model_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.fuel_type_entry.delete(0, 'end')

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
            self.data, self.status, USERNAME = ls.login_func(username=self.username_entry.get(), password=self.password_entry.get(), config=config)
            if self.status is False:
                messagebox.showerror(title="Fail Authenticator", message="Username-ul sau parola sunt gresite.")
            else:
                self.root.destroy()
                PartsManager()
                # aici instantiez noua mea fereastra
        # trebuie afisat ceva cand utilizatorul gresteste parola sau nu completeaza nimic


if __name__ == "__main__":
    # LoginWindow()
    PartsManager()

    # deletes everything from the json file
    data = {}
    with open("AutoDetails.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
