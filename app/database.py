import os
from dotenv import load_dotenv
from dataclasses import dataclass
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# Initialize dotenv
load_dotenv()


@dataclass
class Database:
    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')

    def connect(self):
        """Return connection object after connecting to database."""
        while True:

            try:
                print('Connecting to database...')

                conn = psycopg2.connect(host=self.HOST,
                                        database=self.DATABASE,
                                        user=self.USER,
                                        password=self.PASSWORD,
                                        cursor_factory=RealDictCursor)
                
                print('Database connected successfully!')
                return conn

            except Exception as error:
                print('Connecting to database failed.\nError', error)
                time.sleep(2)
