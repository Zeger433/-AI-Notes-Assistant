from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:0099@localhost:5432/note_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()