import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.mapper import metadata

user = os.getenv('USER', 'user')
password = os.getenv('PASSWORD', 'password')
host = os.getenv('HOST', 'localhost')
port = os.getenv('PORT', '5432')
database = os.getenv('DATABASE', 'test')

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
Session = sessionmaker(engine)
metadata.create_all(engine)
