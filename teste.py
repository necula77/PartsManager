import tkinter as tk

global next_row
next_row = 4

def position_empty_label(row, column):
    # label to position the button better
    empty_label = tk.Label(win, text="      ", font=("Source Code Pro", "14"))
    empty_label.grid(row=row, column=column, pady=10)

def add_table_row():
    global next_row  # Declare next_row as global
    new_row = tk.Entry(win, width=10, fg="gray", font=('Arial', 16, 'bold'))
    new_row.grid(row=next_row, column=0)
    next_row += 1

win = tk.Tk()
win.title("PartsManager")
win.geometry("745x500")

frame = tk.Frame(win)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.columnconfigure(4, weight=1)
frame.columnconfigure(5, weight=1)
frame.columnconfigure(6, weight=1)

frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)
frame.rowconfigure(3, weight=1)
frame.rowconfigure(4, weight=1)
frame.rowconfigure(5, weight=1)

first_row_of_table = tk.Entry(win, width=10, fg="gray", font=('Arial', 16, 'bold'))

position_empty_label(1, 0)
position_empty_label(2, 0)

first_table_row = 3
first_row_of_table.grid(row=first_table_row, column=0)

add_table_row_button = tk.Button(win,
                                 text="Add row",
                                 font=("Arial", "14"),
                                 command=add_table_row)

add_table_row_button.grid(row=1, column=1)

win.mainloop()


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