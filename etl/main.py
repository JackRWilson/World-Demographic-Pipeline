import os

from dynaconf import Dynaconf
from sqlalchemy import create_engine

from etl import ETLProcessor

os.chdir(os.path.dirname(__file__))


def run():

    data_path = "../data/idb5yr.txt"

    def build_engine():
        settings = Dynaconf(envvar_prefix="DB", load_dotenv=True, dotenv_override=True)
        return create_engine(settings.ENGINE_URL, echo=False)

    engine = build_engine()

    with engine.connect() as cnx:
        processor = ETLProcessor(cnx, data_path)
        processor.process()

    engine.dispose()


if __name__ == "__main__":
    run()
