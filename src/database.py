import re
from glob import glob

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from src.config import settings

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


def resolve_table_name(name):
    names = re.split(r"(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_all_models():
    # Import all modules in the models package
    import pkgutil

    # Dynamically discover all classes that inherit from Base
    models = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        glob("src/*", recursive=True)
    ):
        module = loader.find_module(module_name).load_module(module_name)
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, "__bases__") and Base in obj.__bases__:
                models.append(obj)

    return models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
