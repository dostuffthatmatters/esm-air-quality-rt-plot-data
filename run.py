import os
from dotenv import load_dotenv
from rich import print

from supabase_py import create_client, Client
from cerberus import Validator as cerberus_validator

assert ".env" in os.listdir("./")
load_dotenv()
url, key, table = (
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_PUBLIC"),
    os.getenv("SUPABASE_TABLE"),
)
email, password = os.getenv("USER_EMAIL"), os.getenv("USER_PASSWORD")
assert all([x is not None for x in [url, key, table, email, password]])


class Validator:
    __integer = {"type": "integer", "required": True}
    __float = {"type": "float", "required": True, "nullable": True}

    __validator = cerberus_validator(
        {
            "unix-timestamp": __integer,
            "NO2": __float,
            "PM10": __float,
            "PM25": __float,
            "PM1": __float,
            "p": __float,
            "T": __float,
            "HUM": __float,
        }
    )

    @staticmethod
    def check(document):
        if not Validator.__validator.validate(document):
            raise Exception(f"Errors: {Validator.__validator.errors}")
        assert len([k for k in document.keys() if document[k] is not None]) > 1


class DB:
    supabase: Client = create_client(url, key)
    user = supabase.auth.sign_in(email=email, password=password)
    assert user["status_code"] == 200, f"Login not successful, {user}"

    @staticmethod
    def insert_data(data):
        data["unix-timestamp"] = round(time.time())
        Validator.check(data)

        # Only prints the not-None values
        print({k: data[k] for k in data.keys() if data[k] is not None})

        assert DB.supabase.auth.user() is not None
        assert DB.supabase.auth.session() is not None
        response = DB.supabase.table(table).insert(data).execute()
        assert (
            str(response["status_code"])[0] == "2"
        ), f"Insert not successful, {response}"


if __name__ == "__main__":
    import time
    import random

    print(f'Inserting in table {os.environ.get("SUPABASE_TABLE")}')

    while True:

        # None is a valid value (if there is no data for some sensors)
        # If there is not data (all None), just do not send any db reqests.
        DB.insert_data(
            {
                "NO2": round(random.uniform(5, 35), 2),
                "PM10": None,
                "PM25": None,
                "PM1": None,
                "p": None,
                "T": None,
                "HUM": None,
            }
        )
        time.sleep(2)
