import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

pg_pw = os.environ.get("pg_pw")
