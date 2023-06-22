from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f"sqlite:///C:/Users/cferrucci.WIENER-LAB/PycharmProjects/pythonProject/sqlalchemy_with_fastapi/connection/db/sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(engine)

Base = declarative_base()
