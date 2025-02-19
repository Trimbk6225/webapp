from os import getenv
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{getenv('DATABASE_USERNAME')}:{getenv('DATABASE_PASSWORD')}"
        f"@{getenv('DATABASE_HOST')}:{getenv('DATABASE_PORT')}/{getenv('DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{getenv('DATABASE_USERNAME')}:{getenv('DATABASE_PASSWORD')}"
        f"@{getenv('DATABASE_HOST')}:{getenv('DATABASE_PORT')}/test_healthcheckdb"
    )
    TESTING = True