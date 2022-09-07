import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv()) # find key on .env file if not using pipenv
BOT_KEY=os.getenv('BOT_KEY')