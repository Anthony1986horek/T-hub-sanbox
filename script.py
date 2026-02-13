import requests
import pandas as pd
import psycopg2
import json
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

file = 'https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/refs/heads/master/airports.json'



class GetAirports:


    @staticmethod
    def query_to_api():
        info = requests.get(file)
        data = json.loads(info.text)
        return data

    @staticmethod
    def parsing_data():
        df = pd.DataFrame(GetAirports.query_to_api())
        return df

    @staticmethod
    def create_table():
        load_dotenv()
        with psycopg2.connect(
        database='postgres',
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host="127.0.0.1",
        port="5432") as connection:
            cur = connection.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS airports(
            iata TEXT,
            lon FLOAT,
            iso TEXT,
            status INTEGER,
            name TEXT,
            continent TEXT,
            type TEXT,
            lat FLOAT,
            size TEXT);""")

    @staticmethod
    def put_data_into_table():
            load_dotenv()
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/postgres')
            GetAirports.parsing_data().to_sql('airports', engine, if_exists='replace', index=False)


    @staticmethod
    def get_data_from_table():
        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/postgres')
        df = pd.read_sql("""SELECT * FROM airports LIMIT 20;""", engine)
        print(df)


def main():
        if GetAirports.query_to_api():
            GetAirports.parsing_data()
            GetAirports.create_table()
            # GetAirports.put_data_into_table()
            GetAirports.get_data_from_table()

if __name__ == "__main__":
     main()