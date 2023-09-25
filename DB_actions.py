import json
import logging
import psycopg2 as ps
import psycopg2.errors
from psycopg2 import errors as pserrors
from psycopg2.extras import RealDictCursor
import tkinter as tk
from tkinter import messagebox

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                        datefmt="%d-%b-%Y %H:%M:%S",
                        handlers=[
                            logging.FileHandler("app.log"),  # apare intr un fisier
                            logging.StreamHandler()  # apare in consola ca un print
                        ]
                        )


def find_error_code(e):
    psycopg2.errors.lookup(e)
    print('Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e)))


def get_config(file="config.json"):
    try:
        with open(file, "r") as f:
            data = json.loads(f.read())

        return data
    except Exception as e:
        logging.error(f"Exceptie la citirea configului {e}.")
        exit()


CONFIG = get_config()


def insert_in_db(sql_query, logged_user, license_plate, vin, config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                conn.commit()
        logging.info(f"""User {logged_user} a accesat baza de date pentru a modifica datele masinii: {license_plate}, {vin}.""")

        return True

    except SyntaxError as e:

        logging.error(f"Eroare la introducerea in datelor in baza de date. Query-ul a fost scris gresit. \n {e}")

    except Exception as e:

        logging.error(f"Eroare la introducerea datelor in baza de date: {e}")
        exit()


def recieve_from_db(config=CONFIG, vin="", license_plate=""):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                sql_query = f"""select "VIN", "License Plate", "Manufacturer", "Model", "Year",
                               "Engine", "KW", "CMC", "Fuel_Type", "KM"
                               from "Auto_Details"."REGISTERED_CARS"
                               where "VIN"='{vin}' OR "License Plate"='{license_plate}';"""

                cursor.execute(sql_query)
                data = cursor.fetchone()

                return data



    except Exception as e:
        ps.errors.lookup(e)
        logging.error(f"Eroare la autentificare: {e}")
        exit()


def register_part(part_number, part_name, stock, location, price, logged_user, config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""insert into "Parts"."Warehouse"("Part_number", "Part_name", "Stock", "Location","Price")
                                   values ('{part_number}', '{part_name}', '{stock}', '{location}', {price});""")
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo(title="Message",
                                        message=f"Piesa {part_number} a fost adaugata cu succes.")
                    logging.info(
                        f"""User {logged_user} a accesat baza de date pentru a adauga {part_name}, {part_number}.""")

    except pserrors.SyntaxError as e:

        logging.error(f"Eroare la introducerea in datelor in baza de date. Query-ul a fost scris gresit. \n {e}")
        messagebox.showerror(title="Error",
                             message=f"Piesa nu poate fi adugata, va rugam sa verificati datele introduse.")

    except pserrors.UniqueViolation as e:

        logging.error(f"Eroare la introducerea datelor in baza de date, piesa introduse este deja inregistrata. \n {e}")
        messagebox.showerror(title="Error",
                             message=f"Piesa nu poate fi adugata, va rugam sa verificati datele introduse.")

    except Exception as e:
        psycopg2.errors.lookup(e)
        logging.error(f"Eroare la introducerea datelor in baza de date: {e}")
        messagebox.showerror(title="Error",
                             message=f"Piesa nu poate fi adugata, va rugam sa verificati datele introduse.")
        exit()


def remove_part(part_number, logged_user,config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM "Parts"."Warehouse"
                                   WHERE "Part_number" = '{part_number}';""")
                conn.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo(title="Message",
                                               message=f"Piesa {part_number} a fost stearsa cu succes.")
                    logging.info(
                        f"""User {logged_user} a accesat baza de date pentru a sterge piesa {part_number}.""")
                else:
                    messagebox.showerror(title="Error",
                                         message=f"Piesa nu poate fi stearsa, va rugam sa verificati datele introduse.")

    except pserrors.SyntaxError as e:

        logging.error(f"Eroare la stergerea informatiilor din baza de date. Query-ul a fost scris gresit. \n {e}")

    except pserrors.UniqueViolation as e:

        logging.error(f"Eroare la stergerea informatiilor din baza de date, piesa introduse este deja inregistrata. \n {e}")

    except Exception as e:
        psycopg2.errors.lookup(e)
        logging.error(f"Eroare la stergerea informatiilor din baza de date: {e}")
        exit()


def recieve_shipment(part_number, stock_to_add, logged_user, config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""UPDATE "Parts"."Warehouse"
                                   SET "Stock" = "Stock" + '{stock_to_add}'
                                   WHERE "Part_number" = '{part_number}';""")
                conn.commit()

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT "Stock"
                                   FROM "Parts"."Warehouse"
                                   WHERE "Part_number" = '{part_number}';""")

                conn.commit()
                new_stock = cursor.fetchone()

        logging.info(
            f"""User {logged_user} a accesat baza de date
                pentru a modifica stockul din depozit pentru {part_number}, acesta fiind acum {new_stock[0]} bucati.""")

        return True

    except pserrors.SyntaxError as e:

        logging.error(f"Error whilst sending data to data base. Query is wrong. \n {e}")

    except pserrors.InvalidTextRepresentation as e:

        logging.error(f"Error whilst sending data to data base, 'Stock' box cannot be empty. \n {e}")
        messagebox.showerror(title="Error",
                             message=f"The stock cannot be recieved. Please input something in the 'Stock' box.")

    except TypeError as e:

        logging.error(f"Error occured. 'Part number' box cannot be empty.")
        messagebox.showerror(title="Error",
                             message=f"All fields must be completed.")

    except Exception as e:
        psycopg2.errors.lookup(e)
        logging.error(f"Error whilst sending data to data base: {e}")
        exit()


def recieve_info_abt_part(part_number, config=CONFIG):

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""SELECT "Part_name", "Stock", "Price", "Location"
                                FROM "Parts"."Warehouse"
                                WHERE "Part_number" = '{part_number}';"""

                cursor.execute(sql_query)
                data = cursor.fetchone()

                return data

    except Exception as e:
        logging.error(f"Eroare la identificarea piesei: {e}.")

def remove_stock(part_number, stock_to_remove, config=CONFIG):

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""UPDATE "Parts"."Warehouse"
                                   SET "Stock" = "Stock" - '{stock_to_remove}'
                                   WHERE "Part_number" = '{part_number}';"""
                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error occured: {e}")


def check_for_car(vin, license_plate, config=CONFIG):

    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT "VIN", "License Plate"
                               from "Auto_Details"."REGISTERED_CARS"
                               where "VIN"='{vin}' OR "License Plate"='{license_plate}';""")
            data = cursor.fetchone()

    if data is None:
        return False
    else:
        return True


def delete_car_info(vin, license_plate, logged_user, config=CONFIG):

    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:

            sql_query = f"""DELETE FROM "Auto_Details"."REGISTERED_CARS"
                            WHERE "VIN" = '{vin}' OR "License Plate" = '{license_plate}';"""

            cursor.execute(sql_query)
            if cursor.rowcount > 0:
                tk.messagebox.showinfo(title="Succes", message="The car's info was deleted sucesfully!")
            else:
                tk.messagebox.showerror(title="Error", message="The car's info could not be deleted!")


# if __name__ == '__main__':
#     register_part("0102C-13256", "Electromotor", 3, "A-12", 780.7, "necula77")