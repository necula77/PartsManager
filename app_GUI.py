import tkinter as tk
from tkinter import messagebox
import login_sequence as ls
from login_sequence import config
import psycopg2 as ps
import logging
import DB_actions
import webbrowser

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                        datefmt="%d-%b-%Y %H:%M:%S",
                        handlers=[
                            logging.FileHandler("app.log"),  # apare intr un fisier
                            logging.StreamHandler()  # apare in consola ca un print
                        ]
                        )


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

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)

        # Table

        self.create_table(5, 6, start_row=3)

        # Buttons

        self.auto_details_button = tk.Button(self.win, text="Auto Details", font=("Arial", "14"), command=AutoDetails)
        self.auto_details_button.grid(row=0, column=0, pady=20)
        self.auto_details_button.configure(borderwidth=1, font='Calibri 10 bold')

        self.open_tec_doc_button = tk.Button(self.win, text="TecDoc", font=("Arial", "14"), command=self.open_tec_doc)
        self.open_tec_doc_button.grid(row=0, column=1, pady=20)
        self.open_tec_doc_button.configure(borderwidth=1, font='Calibri 10 bold')


        # widgets declaration

        self._label = tk.Label(self.win, text="", font=("Arial", "14"))
        self._entry = tk.Entry(self.win, width=15, font=("Arial", "14"))

        # widgets rendering

        # self._label.grid(row=, column=, pady=10)
        # self._entry.grid(row=, column=, pady=5)

        self.win.mainloop()

    def create_table(self, row, column, start_row=0):

        for i in range(row):

            for j in range(column):
                table = tk.Entry(self.win, width=10, fg="gray", font=('Arial', 16, 'bold'))
                table.grid(row=i + start_row, column=j)

    def open_tec_doc(self):
        webbrowser.open('https://web.tecalliance.net/tecdocsw/ro/login')


class AutoDetails:

    def __init__(self):

        self.config = config
        self.root = tk.Tk()
        self.root.title("Auto Details")
        self.root.geometry("535x320+550+270")
        # self.root.wm_attributes("-topmost", True)

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

        self.root.mainloop()


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

        # sql_query = f"""insert into "Auto_Details"."REGISTERED_CARS"
        #                  ("VIN", "License Plate", "Manufacturer", "Model", "Year",
        #                  "Engine", "KW", "CMC", "Fuel_Type", "KM")
        #                  values ('{self.vin_entry.get()}', '{self.license_plate_entry.get()}',
        #                  '{self.make_entry.get()}', '{self.model_entry.get()}', '{self.year_entry.get()}',
        #                  '{self.engine_entry.get()}', '{self.kw_entry.get()}', '{self.cc_entry.get()}',
        #                  '{self.fuel_type_entry.get()}', '{self.km_entry.get()}');"""

        status = DB_actions.insert_in_db(config=config, sql_query=sql_query,
                                         logged_user='x', license_plate=self.license_plate_entry.get(),
                                         vin=self.vin_entry.get())

        if status is True:
            messagebox.showinfo(title="Message", message="Datele au fost introduse cu succes.")

    def retrieve_btn_cmd(self):

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

        return data


class LoginWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.geometry("400x300+550+270")

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
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", "14"))
        self.password_entry = tk.Entry(self.root, width=15, font=("Arial", "14"), show="*")

        # widgets rendering
        self.hello_label.grid(row=0, column=1, padx=90)
        self.username_label.grid(row=1, column=1, pady=10)
        self.username_entry.grid(row=2, column=1, pady=5)
        self.password_label.grid(row=3, column=1, pady=10)
        self.password_entry.grid(row=4, column=1, pady=5)

        self.root.mainloop()

    def login_btn_cmd(self):

        # authorization_level = ls.login_func(username=self.username_entry.get(), password=self.password_entry.get(), config=config)[0]
        # self.status = authorization_level[1]
        if self.username_entry.get() and self.password_entry.get():
            self.data, self.status = ls.login_func(username=self.username_entry.get(), password=self.password_entry.get(), config=config)
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
