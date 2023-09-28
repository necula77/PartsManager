import psycopg2 as ps
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                    datefmt="%d-%b-%Y %H:%M:%S",
                    handlers=[
                        logging.FileHandler("app.log"),  # apare intr un fisier
                        logging.StreamHandler()  # apare in consola ca un print
                    ]
                    )

def get_config(file="config.json"):
    try:
        with open(file, "r") as f:
            data = json.loads(f.read())

        return data
    except Exception as e:
        logging.error(f"Error whilst reading config: {e}.")
        exit()


CONFIG = get_config()


def delete_public_schema(config=CONFIG):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = 'DROP SCHEMA IF EXISTS "public";'

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")
        exit()


def create_schema_and_table_for_login(config=CONFIG):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = 'CREATE SCHEMA IF NOT EXISTS "Authorization";'

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")
        exit()

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = """CREATE TABLE IF NOT EXISTS "Authorization"."LOGIN_INFO" (
                               user_id SERIAL PRIMARY KEY,
                               first_name VARCHAR(50) NOT NULL,
                               last_name VARCHAR(50) NOT NULL,
                               username VARCHAR(20) NOT NULL,
                               password VARCHAR(100) NOT NULL,
                               "function" VARCHAR(20) CHECK ("function" IN ('Consilier', 'Piesar', 'Sef atelier', 'Admin')),
                               starting_date DATE NOT NULL DEFAULT CURRENT_DATE,
                               CONSTRAINT unique_username UNIQUE (username)
                               );"""

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = """INSERT INTO "Authorization"."LOGIN_INFO"
                            (first_name, last_name, username, password, "function", starting_date)
                            VALUES ('temporary', 'temporary', 'admin', 'admin', 'Admin', CURRENT_DATE);"""

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")


def create_schema_and_table_for_cars(config=CONFIG):

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = 'CREATE SCHEMA IF NOT EXISTS "Auto_Details";'

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")
        exit()

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = """create table if not exists "Auto_Details"."REGISTERED_CARS" (
                               "VIN" VARCHAR(17) primary key CHECK (NOT ("VIN" ~* '[OIoi]')),
                               "License Plate" VARCHAR(10) not null,
                               "Manufacturer" VARCHAR(30) not null,
                               "Model" VARCHAR(30) not null,
                               "Year" INT not null,
                               "Engine" VARCHAR(10) not null,
                               "KW" INT,
                               "CMC" INT,
                               "Fuel_Type" VARCHAR(40),
                               "KM" INT not null
                               );"""

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")


def create_schema_and_table_for_parts(config=CONFIG):

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = 'CREATE SCHEMA IF NOT EXISTS "Parts";'

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")
        exit()

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = """create table if not exists "Parts"."Warehouse"(
                               "Part_number" VARCHAR(20) primary key,
                               "Part_name" VARCHAR(30) not null,
                               "Stock" INT not null,
                               "Location" VARCHAR(20) not null,
                               "Price" FLOAT not null,
                               CONSTRAINT unique_part_number UNIQUE ("Part_number")
                               );"""

                cursor.execute(sql_query)
                conn.commit()

    except Exception as e:

        logging.error(f"Error whilst creating DataBase: {e}")


def create_data_base():

    create_schema_and_table_for_login()
    create_schema_and_table_for_cars()
    create_schema_and_table_for_parts()
    delete_public_schema()
    logging.info(f"DataBase was successfully created!")





