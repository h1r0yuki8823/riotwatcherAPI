import os
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())
RIOT_API_KEY = os.environ.get('API_KEY')
RIOT_API_KEY2 = 'RGAPI-03d3369b-59c7-45a2-93e8-b307fdb2e7ee'