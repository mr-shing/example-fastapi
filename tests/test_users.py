from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host_name}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_root():
    res = client.get("/")
    print(res.json().get('Message'))
    assert res.json().get('Message') == 'Hello World'
    assert res.status_code == 200


def test_create_user():
    res = client.post('/users/', json={"email": "hello15235586@gmail.com", "password": "password1234"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert res.status_code == 201
