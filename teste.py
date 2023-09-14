import tkinter as tk
from tkinter import *
from tkinter import messagebox
import login_sequence as ls
from login_sequence import config
import logging
import DB_actions
import webbrowser
from PIL import Image, ImageTk
import json
from functools import partial

USERNAME = ""

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                    datefmt="%d-%b-%Y %H:%M:%S",
                    handlers=[
                        logging.FileHandler("app.log"),  # appears in a file
                        logging.StreamHandler()  # appears in console as print
                    ]
                    )


def center_window(win):
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


class PartsManager:

    global max_row

    next_row = 3
    max_row = 0

    def __init__(self):

        self.win = tk.Tk()
        self.win.title("PartsManager")

        self.win.geometry("745x500")
        center_window(self.win)

        self.win.resizable(False, False)

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

        self.entry_widgets = []

        self.add_table_row()

        self.auto_details_button = tk.Button(self.win,
                                             text="Auto Details",
                                             command=self.auto_details)
        self.auto_details_button.grid(row=0, column=0, pady=20)
        self.auto_details_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.open_tec_doc_button = tk.Button(self.win,
                                             text="TecDoc",
                                             command=self.open_tec_doc)
        self.open_tec_doc_button.grid(row=0, column=1, pady=20)
        self.open_tec_doc_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.receive_shipment_button = tk.Button(self.win,
                                                 text="Receive Shipment",
                                                 command=self.receive_shipment)
        self.receive_shipment_button.grid(row=0, column=2, pady=20)
        self.receive_shipment_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.manage_parts_button = tk.Button(self.win,
                                              text="Manage Parts",
                                              command=self.manage_parts)
        self.manage_parts_button.grid(row=0, column=3, pady=20)
        self.manage_parts_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.clear_table_button = tk.Button(self.win,
                                            text="Clear table",
                                            command=self.clear_table)
        self.clear_table_button.grid(row=0, column=4, pady=20)
        self.clear_table_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.add_table_row_button = tk.Button(self.win,
                                              text="Add row",
                                              command=self.add_table_row)
        self.add_table_row_button.grid(row=2, column=6, pady=40, sticky="ne")
        self.add_table_row_button.configure(borderwidth=1, font='Calibri 12 bold')

        self.part_name_label = tk.Label(self.win, text="Part Name", font=("Source Code Pro", "14"))
        self.part_number_label = tk.Label(self.win, text="Part Number", font=("Source Code Pro", "14"))
        self.stock_label = tk.Label(self.win, text="Stock", font=("Source Code Pro", "14"))
        self.price_label = tk.Label(self.win, text="Price", font=("Source Code Pro", "14"))
        self.location_in_warehouse_label = tk.Label(self.win, text="Location", font=("Source Code Pro", "14"))

        self.part_number_label.grid(row=2, column=0, pady=10)
        self.part_name_label.grid(row=2, column=1, pady=10)
        self.stock_label.grid(row=2, column=2, pady=10)
        self.price_label.grid(row=2, column=3, pady=10)
        self.location_in_warehouse_label.grid(row=2, column=4, pady=10)

        self.entry_widgets[0][0].bind('<Return>', self.fill_table_entries)

        self.win.mainloop()
        self.status = False

    def add_table_row(self):
        global max_row

        if max_row < 10:
            row_widgets = []
            for i in range(5):
                new_row = tk.Entry(self.win, width=10, fg="black", font=('Arial', 15, 'bold'))
                new_row.grid(row=self.next_row, column=i)

                if i == 0:
                    new_row.bind('<Return>', self.fill_table_entries)

                row_widgets.append(new_row)

            self.entry_widgets.append(row_widgets)
            self.next_row += 1
            max_row += 1
        else:
            tk.messagebox.showinfo(title="Maximum rows",
                                   message="Maximum number of rows has been reached, please create a new app.")

    def clear_table(self):
        global max_row

        for row_widgets in self.entry_widgets:
            for entry in row_widgets:
                entry.grid_remove()
        self.entry_widgets.clear()

        self.add_table_row()
        max_row = 0

    def auto_details(self):
        pass

    def open_tec_doc(self):
        webbrowser.open(config.TEC_DOC_URL)

    def receive_shipment(self):
        pass

    def manage_parts(self):
        pass

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


class RecieveShipment:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Recieve Shipment")
        self.root.geometry("280x180")
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


class ManageParts:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manage Parts")
        self.root.geometry("535x320+550+270")
        center_window(self.root)

        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=2)
        self.root.columnconfigure(4, weight=2)

        # Buttons

        self.send_button = tk.Button(self.root, text="Send", font=("Arial", "14"), command=self.send_btn_cmd)
        self.send_button.grid(row=7, column=4, pady=20)

        self.retrieve_data_button = tk.Button(self.root, text="Retrieve data", font=("Arial", "14"))
        self.retrieve_data_button.grid(row=7, column=3, pady=20)

        self.clear_button = tk.Button(self.root, text="Clear", font=("Arial", "14"))
        self.clear_button.grid(row=7, column=2, pady=20)

        self.remove_button = tk.Button(self.root, text="Remove", font=("Arial", "14"), command=self.remove_btn_cmd)
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

    def remove_btn_cmd(self):

        part_number = self.part_number_entry.get()

        status = DB_actions.remove_part(part_number=part_number,
                                        logged_user=USERNAME)

        if status is True:
            return messagebox.showinfo(title="Message",
                                       message=f"Piesa {part_number} a fost stearsa cu succes."),\
                   self.root.destroy()
        else:
            return messagebox.showerror(title="Error",
                                        message=f"Piesa nu poate fi stearsa, va rugam sa verificati datele introduse.")


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
