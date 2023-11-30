from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

# without docker
#SQLALCHEMY_DATABASE_URL = "postgresql://root:root@localhost/medicine"

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
