import json
import logging
import psycopg2 as ps
import psycopg2.errors
from psycopg2 import errors as pserrors
import requests
from psycopg2.extras import RealDictCursor
import app_GUI

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
        logging.error(f"Eroare la autentificare: {e}")
        exit()


def register_part(part_number, part_name, stock, location, price, logged_user, config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""insert into "Parts"."Warehouse"("Part_number", "Part_name", "Stock", "Location","Price")
                                   values ('{part_number}', '{part_name}', '{stock}', '{location}', {price});""")
                conn.commit()
        logging.info(
            f"""User {logged_user} a accesat baza de date pentru a adauga {part_name}, {part_number}.""")

        return True

    except pserrors.SyntaxError as e:

        logging.error(f"Eroare la introducerea in datelor in baza de date. Query-ul a fost scris gresit. \n {e}")

    except pserrors.UniqueViolation as e:

        logging.error(f"Eroare la introducerea datelor in baza de date, piesa introduse este deja inregistrata. \n {e}")

    except Exception as e:
        psycopg2.errors.lookup(e)
        logging.error(f"Eroare la introducerea datelor in baza de date: {e}")
        exit()


def recieve_shipment(part_number, stock, logged_user, config=CONFIG):
    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""UPDATE "Parts"."Warehouse"
                                   SET "Stock" = {stock}
                                   WHERE "Part_number" = '{part_number}';""")
                conn.commit()
        logging.info(
            f"""User {logged_user} a accesat baza de date
                pentru a modifica stockul din depozit pentru {part_number}, acesta fiind acum {stock}.""")

        return True

    except pserrors.SyntaxError as e:

        logging.error(f"Eroare la introducerea in datelor in baza de date. Query-ul a fost scris gresit. \n {e}")

    except pserrors.UniqueViolation as e:

        logging.error(f"Eroare la introducerea datelor in baza de date, piesa introduse este deja inregistrata. \n {e}")

    except Exception as e:
        psycopg2.errors.lookup(e)
        logging.error(f"Eroare la introducerea datelor in baza de date: {e}")
        exit()


if __name__ == '__main__':
    register_part("0102C-13256", "Electromotor", 3, "A-12", 780.7, "necula77")

