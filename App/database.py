from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData


# creating the database
db_host = "localhost"
db_name = "postgres"
db_pass = "4895"
db_user = "postgres"

engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}")
Base = declarative_base()

Session = sessionmaker(bind=engine)
