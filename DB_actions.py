import json
import logging
import psycopg2 as ps
from psycopg2 import errors
import requests


LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                        datefmt="%d-%b-%Y %H:%M:%S",
                        handlers=[
                            logging.FileHandler("app_log.txt"),  # apare intr un fisier
                            logging.StreamHandler()  # apare in consola ca un print
                        ]
                        )


class Registered_Cars():

    def __init__(self):
        self.config = get_config()

    def insert_in_db(self):
        pass


    def recieve_from_db(self, vin="", license_plate=""):
        try:
            with ps.connect(**self.config) as conn:
                with conn.cursor() as cursor:
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


def get_config(file="config.json"):
    try:
        with open(file, "r") as f:
            data = json.loads(f.read())

        return data
    except Exception as e:
        logging.error(f"Exceptie la citirea configului {e}.")
        exit()



