import pandas as pd
import pycountry_convert as pc
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

continent_names = {
    "AF": "Africa",
    "AS": "Asia",
    "EU": "Europe",
    "NA": "North America",
    "OC": "Oceania",
    "SA": "South America",
}

country_continents_mapping = {
    "SX": "NA",
    "TL": "AS",
    "XG": "AS",
    "XW": "AS",
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


def get_continent(country_code):
    try:
        if isinstance(country_code, str) and len(country_code) == 2:
            alpha2_code = country_code
        else:
            alpha2_code = pc.country_name_to_country_alpha2(country_code)

        if alpha2_code in country_continents_mapping:
            continent_code = country_continents_mapping[alpha2_code]
        else:
            continent_code = pc.country_alpha2_to_continent_code(alpha2_code)
        return continent_names.get(continent_code, "Unknown")
    except (KeyError, ValueError):
        return "Unknown"


engine = build_engine()

country_df = extract_data("country", engine)
country_df["continent"] = country_df["country_code"].apply(get_continent)
age_df = extract_data("age", engine)
demo_df = extract_data("demographics", engine)
age_demo_df = extract_data("age_demographic", engine)

engine.dispose()
