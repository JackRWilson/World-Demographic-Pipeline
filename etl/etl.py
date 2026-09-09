import pandas as pd
from country_mapping import country_codes


class TransformCountry:
    def transform(self, df):
        df = self._map_country_names(df)
        df = self._drop_extra_cols(df)
        df = self._drop_duplicates(df)
        df = self._rename_cols(df)
        df = self._correct_data_types(df)
        return df

    def _map_country_names(self, df):
        df = df.copy()
        df["country_name"] = df["GEO_ID"].str[9:11].map(country_codes)
        df["country_code"] = df["GEO_ID"].str[9:11]
        return df

    def _drop_extra_cols(self, df):
        return df[["country_code", "country_name", "AREA_KM2"]]

    def _drop_duplicates(self, df):
        return df.drop_duplicates(subset=["country_name"])

    def _rename_cols(self, df):
        return df.rename(columns={"AREA_KM2": "area_km2"})

    def _correct_data_types(self, df):
        df["area_km2"] = df["area_km2"].astype("Int64")
        return df


class ETLProcessor:
    def __init__(self, cnx, data_path):
        self._cnx = cnx
        self._data_path = data_path

    def _extract_demographics(self):
        return pd.read_csv(self._data_path, delimiter="|")

    def process(self):
        print("Extract...")
        df = self._extract_demographics()
        print(df.head())
        print(f"Raw data shape: {df.shape}\n")

        print("Transform...")
        country = TransformCountry().transform(df)
        print(country.head())
        print(country.shape)

        # print("Load...")

        print("Complete.")
