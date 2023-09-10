from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host_name}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# while True:
#     try:
#         connect = psycopg2.connect(host='localhost', database='fastapi', user='json', password='MyPassword',
#                                    cursor_factory=RealDictCursor)
#         cursor = connect.cursor()
#         break
#     except Exception as error:
#         print('Connect to database was failed')
#         print("Error", error)
#         time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
