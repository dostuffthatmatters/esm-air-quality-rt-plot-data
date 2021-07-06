import os
from dotenv import load_dotenv
from rich import print

from supabase_py import create_client, Client
from cerberus import Validator as cerberus_validator

assert('.env' in os.listdir('./'))
load_dotenv()
assert(os.getenv('SUPABASE_URL') != None)
assert(os.getenv('SUPABASE_SECRET') != None)
assert(os.getenv('SUPABASE_TABLE') != None)


class Validator:
    __integer = {'type': 'integer', 'required': True}
    __float = {'type': 'float', 'required': True, 'nullable': True}

    __validator = cerberus_validator({
        'unix-timestamp': __integer,
        'NO2': __float,
        'PM10': __float,
        'PM25': __float,
        'PM1': __float,
        'p': __float,
        'T': __float,
        'HUM': __float,
    })
    

    @staticmethod
    def execute(document):
        if not Validator.__validator.validate(document):
            raise Exception(
                f'Errors: {Validator.__validator.errors}'
            )
        assert(len([k for k in document.keys() if document[k] is not None]) > 1)

class DB:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_SECRET")
    table: str = os.environ.get("SUPABASE_TABLE")
    supabase: Client = create_client(url, key)

    @staticmethod
    def insert_data(data):
        data["unix-timestamp"] = round(time.time())
        Validator.execute(data)

        # Only prints the not-None values
        print({k: data[k] for k in data.keys() if data[k] is not None})
        
        try:
            insertedData = DB.supabase.table(DB.table).insert(data).execute()
            assert (len(insertedData.get("data", [])) > 0)
        except:
            raise Exception("Insert could not be performed")


if __name__ == '__main__':
    import time
    import random

    print(f'Inserting in table {os.environ.get("SUPABASE_TABLE")}')

    while True:
        
        # None is a valid value (if there is no data for some sensors)
        # If there is not data (all None), just do not send any db reqests.
        DB.insert_data({
            'NO2': round(random.uniform(5, 35), 2),
            'PM10': None,
            'PM25': None,
            'PM1': None,
            'p': None,
            'T': None,
            'HUM': None,
        })
        time.sleep(2)
    