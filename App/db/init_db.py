from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
# creating the database
# database configuration
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_pass = os.getenv('DB_PASS')
db_user = os.getenv('DB_USER')

# connect to database
engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}")

#declarative_base will  returns a class.
Base = declarative_base()


SessionLocal = sessionmaker(bind=engine)


