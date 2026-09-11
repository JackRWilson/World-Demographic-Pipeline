import pandas as pd
from dynaconf import Dynaconf
from sqlalchemy import create_engine

major_recessions = {
    "1981-1982 Recession": [1981, 1982],
    "Great Recession": [2007, 2008, 2009],
    "COVID-19 Recession": [2020],
}

age_midpoints = {
    "15-19": 17,
    "20-24": 22,
    "25-29": 27,
    "30-34": 32,
    "35-39": 37,
    "40-44": 42,
    "45-49": 47,
}


def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True, dotenv_override=True)
    return create_engine(settings.ENGINE_URL, echo=False)


def extract_data(table_name, engine):
    return pd.read_sql(f"select * from {table_name};", engine)


def get_filtered_countries(df, countries):
    if isinstance(countries, str):
        countries = [countries]
    return df[df["country_name"].isin(countries)]


def get_filtered_recession_years(df, recession, additional_years=3):
    years = major_recessions[recession]
    start = min(years)
    end = max(years)
    return df[df["year"].between(start - additional_years, end + additional_years)]


engine = build_engine()

country_df = extract_data("country", engine)
age_df = extract_data("age", engine)
demo_df = extract_data("demographics", engine)
age_demo_df = extract_data("age_demographic", engine)

engine.dispose()
