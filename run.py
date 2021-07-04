from dotenv import load_dotenv
import os
from supabase_py import create_client, Client
from cerberus import Validator as cerberus_validator
import time
import math
import random

assert('.env' in os.listdir('./'))
load_dotenv()
assert(os.getenv('SUPABASE_URL') != None)
assert(os.getenv('SUPABASE_SECRET') != None)


class Validator:
    __integer = {'type': 'integer', 'required': True}
    __float = {'type': 'float', 'required': True, 'nullable': True}

    __validator = cerberus_validator({
        'unix-timestamp': __integer,
        'NO2': __float,
        'PM1': __float,
        'PM25': __float,
        'PM10': __float,
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

class DB:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_SECRET")
    supabase: Client = create_client(url, key)

    @staticmethod
    def insert_data(data):
        data["unix-timestamp"] = round(time.time())
        Validator.execute(data)

        print(data)
        
        try:
            insertedData = DB.supabase.table("air-quality-timeseries").insert(data).execute()
            assert (len(insertedData.get("data", [])) > 0)
        except:
            raise Exception("Insert could not be performed")


if __name__ == '__main__':
    while True:
        DB.insert_data({
            'NO2': None,
            'PM1': None,
            'PM25': None,
            'PM10': None,
            'p': None,
            'T': round(random.uniform(10.5, 75.5), 2),
            'HUM': None,
        })
        time.sleep(5)
    