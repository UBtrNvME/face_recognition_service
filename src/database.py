import importlib
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
    # Dynamically discover all classes that inherit from Base
    models = []
    # Iterate through all modules in the project
    print(glob("src/*/models.py"))
    for module_name in glob("src/*/models.py"):
        module_path = module_name.replace("/", ".").rsplit(".", maxsplit=1)[0]

        # Import the module dynamically
        module = importlib.import_module(module_path, "models")

        # Iterate through all names in the module
        for name in dir(module):
            obj = getattr(module, name)

            # Check if the object is a class inheriting from Base
            if hasattr(obj, "__bases__") and Base in obj.__bases__:
                models.append(obj)

    return models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
