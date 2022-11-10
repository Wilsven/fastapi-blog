# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## Using the postgres driver
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="qweszqsxzaw96",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as e:
#         print("Connection to database failed!")
#         print("Error: ", e)
#         time.sleep(2)
