import json
import logging
import psycopg2 as ps
from psycopg2 import errors as pserrors


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

                if data == None:
                    status = False

                    print("Username-ul sau parola sunt gresite. Va rugam sa incercati din nou.")
                    return data, status, username
                else:
                    logging.info(f"Utilizatorul {username} s-a logat cu succes.")
                    status = True
                    return data, status, username

    except Exception as e:
        logging.error(f"Eroare la autentificare: {e}")
        exit()


def signup_func(username, password, first_name, last_name, function, config=CONFIG):

    try:

        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:

                sql_query = f"""INSERT INTO "Authorization"."LOGIN_INFO"(first_name, last_name, username, password,
                                "function", starting_date)
                                VALUES('{first_name}', '{last_name}', '{username}', '{password}',
                                 '{function}', CURRENT_DATE);"""

                cursor.execute(sql_query)
                conn.commit()
        logging.info(f"User: {username} a fost adaugat in baza de date, NUME: {last_name} PRENUME: {first_name}.")

    except pserrors.UniqueViolation:

        logging.error(f"Username-ul: {username}, exista deja, va rugam sa alegeti altul.")
        conn.rollback()

    except Exception as e:

        logging.error(f"Eroare la inregistrare: {e}")
        exit()


config = get_config("config.json")

# username = input("Username: ")
# password = input("Password: ")
#
# # data = login_sequence(username, password, config)
# # print(data)
#
# signup_func("alex", "necula04", "JOHN", "DOE", "Piesar", "Mediu", config)

