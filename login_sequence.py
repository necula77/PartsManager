import json
import logging
import psycopg2 as ps
from psycopg2 import errors as pserrors
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


def get_config(file):
    try:
        with open(file, "r") as f:
            data = json.loads(f.read())

        return data
    except Exception as e:
        logging.error(f"Exceptie la citirea configului {e}.")
        exit()


CONFIG = get_config("config.json")


def login_func(username, password, config=CONFIG):
    # status = None

    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"""SELECT first_name, last_name, function FROM "Authorization"."LOGIN_INFO"
                                WHERE username = '{username}' AND password = '{password}';"""

                cursor.execute(sql_query)
                data = cursor.fetchone()
                # authorization_level = data[2]

                if cursor.rowcount > 0:
                    function = data[2]

                    logging.info(f"Utilizatorul {username} s-a logat cu succes.")

                    status = True

                else:
                    status = False
                    function = ""

                    print("Username-ul sau parola sunt gresite. Va rugam sa incercati din nou.")

                return status, function, username

                # if data == None:
                #     status = False
                #
                #     print("Username-ul sau parola sunt gresite. Va rugam sa incercati din nou.")
                #     return data, status, username
                # else:
                #     logging.info(f"Utilizatorul {username} s-a logat cu succes.")
                #     status = True
                #     return data, status, username

    except Exception as e:
        logging.error(f"Eroare la autentificare: {e}")


def signup_func(username, password, first_name, last_name, function, logged_user,  config=CONFIG):

    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""INSERT INTO "Authorization"."LOGIN_INFO"(first_name, last_name, username, password,
                                "function", starting_date)
                                VALUES('{first_name}', '{last_name}', '{username}', '{password}',
                                 '{function}', CURRENT_DATE);"""

                cursor.execute(sql_query)
                conn.commit()
        logging.info(f"User: {username}, NUME: {last_name} PRENUME: {first_name}"
                     f" a fost adaugat in baza de date de catre '{logged_user}'.")

    except pserrors.UniqueViolation:

        logging.error(f"Username-ul: {username}, exista deja, va rugam sa alegeti altul.")
        conn.rollback()

    except pserrors.CheckViolation as e:
        logging.error(f"Campurile nu au fost completate corect!")

    except pserrors.StringDataRightTruncation as e:
        logging.error(f"Una dintre valorile introduse este prea lunga!")

    except Exception as e:
        pserrors.lookup(e)
        logging.error(f"Eroare la inregistrare: {e}")


def delete_user(username, first_name, last_name, logged_user, config=CONFIG):

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""DELETE FROM "Authorization"."LOGIN_INFO"
                                WHERE "username" = '{username}' AND "first_name" = '{first_name}'
                                 AND "last_name" = '{last_name}';"""

                cursor.execute(sql_query)
                if cursor.rowcount > 0:
                    status = True
                    tk.messagebox.showinfo(title="Succes", message=f"User: {username} has been deleted.")
                else:
                    tk.messagebox.showerror(title="Fail", message="User could not be deleted.")
                    status = False

    except Exception as e:
        print(e)


def verify_if_user_exists(username, config=CONFIG):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""SELECT "user_id" FROM "Authorization"."LOGIN_INFO"
                                WHERE "username"='{username}';"""

                cursor.execute(sql_query)
                data = cursor.fetchone()

                return data

    except Exception as e:
        print(e)


def edit_user_info(user_id, new_username, password, first_name, last_name, function, logged_user, config=CONFIG):

    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""UPDATE "Authorization"."LOGIN_INFO"
                                SET "username" = '{new_username}', "password" = '{password}', function = '{function}',
                                "first_name" = '{first_name}', "last_name" = '{last_name}'
                                WHERE "user_id" = '{user_id}';"""

                cursor.execute(sql_query)
                conn.commit()
                if cursor.rowcount > 0:
                    tk.messagebox.showinfo(title="Succes",
                                           message=f"User: {user_id} has been modified in the database, LAST "
                                                   f"NAME: {last_name}, FIRST NAME: {first_name}, USERNAME: {new_username}.")
                else:
                    tk.messagebox.showerror(title="Fail", message="User could not be edited.")

        logging.info(f"""User: {user_id},NUME: {last_name} PRENUME: {first_name} USERNAME: {new_username}
                          a fost editat in baza de date de catre '{logged_user}'.""")

    except pserrors.UniqueViolation:

        logging.error(f"Username-ul: {new_username}, exista deja, va rugam sa alegeti altul.")
        conn.rollback()

    except pserrors.CheckViolation as e:
        logging.error(f"Campurile nu au fost completate corect!")

    except pserrors.StringDataRightTruncation as e:
        logging.error(f"Una dintre valorile introduse este prea lunga!")

    except Exception as e:
        pserrors.lookup(e)
        logging.error(f"Eroare la inregistrare: {e}")


config = get_config("config.json")

# username = input("Username: ")
# password = input("Password: ")
#
# # data = login_sequence(username, password, config)
# # print(data)
#
# signup_func("alex", "necula04", "JOHN", "DOE", "Piesar", "Mediu", config)

