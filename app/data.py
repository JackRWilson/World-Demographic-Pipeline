import pandas as pd
from dynaconf import Dynaconf
from sqlalchemy import create_engine


def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True, dotenv_override=True)
    return create_engine(settings.ENGINE_URL, echo=False)


def extract_data(table_name, engine):
    return pd.read_sql(f"select * from {table_name};", engine)


def get_filtered_countries(df, countries):
    if isinstance(countries, str):
        countries = [countries]
    return df[df["country_name"].isin(countries)]


engine = build_engine()

country_df = extract_data("country", engine)
age_df = extract_data("age", engine)
demo_df = extract_data("demographics", engine)
age_demo_df = extract_data("age_demographic", engine)

engine.dispose()
