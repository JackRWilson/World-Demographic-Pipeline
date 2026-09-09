import pandas as pd
from country_mapping import country_codes

age_cols = [
    "ASFR15_19",
    "ASFR20_24",
    "ASFR25_29",
    "ASFR30_34",
    "ASFR35_39",
    "ASFR40_44",
    "ASFR45_49",
    "BIRTHS15_19",
    "BIRTHS20_24",
    "BIRTHS25_29",
    "BIRTHS30_34",
    "BIRTHS35_39",
    "BIRTHS40_44",
    "BIRTHS45_49",
]


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


class TransformDemographics:
    def transform(self, df):
        df = self._map_country_code(df)
        df = self._drop_extra_cols(df)
        df = self._rename_cols(df)
        df = self._correct_data_types(df)
        return df

    def _map_country_code(self, df):
        df = df.copy()
        df["country_code"] = df["GEO_ID"].str[9:11]
        return df

    def _drop_extra_cols(self, df):
        return df[
            [
                "#YR",
                "GR",
                "POP",
                "BIRTHS",
                "DEATHS",
                "NATINCR",
                "NIM",
                "NMR",
                "RNI",
                "E0",
                "E0_F",
                "E0_M",
                "country_code",
            ]
        ]

    def _rename_cols(self, df):
        return df.rename(
            columns={
                "#YR": "year",
                "GR": "growth_rate",
                "POP": "population",
                "BIRTHS": "yearly_births",
                "DEATHS": "yearly_deaths",
                "NATINCR": "natural_increase",
                "NIM": "net_migrants",
                "NMR": "net_migration_rate",
                "RNI": "rate_natural_increase",
                "E0": "le_at_birth",
                "E0_F": "female_le_at_birth",
                "E0_M": "male_le_at_birth",
            }
        )

    def _correct_data_types(self, df):
        int64_cols = [
            "yearly_births",
            "yearly_deaths",
            "natural_increase",
            "net_migrants",
        ]
        for col in int64_cols:
            df[col] = df[col].astype("Int64")
        return df


class TransformAge:
    def transform(self):
        return pd.DataFrame(
            {
                "age_range": [
                    "15-19",
                    "20-24",
                    "25-29",
                    "30-34",
                    "35-39",
                    "40-44",
                    "45-49",
                ]
            }
        )


class TransformAgeDemographic:
    def transform(self, df):
        df = self._map_country_code(df)
        df = self._drop_extra_cols(df)
        df = self._drop_na_rows(df)
        df = self._convert_wide_to_long(df)
        df = self._hyphenate_age_range(df)
        df = self._rename_cols(df)
        return df

    def _map_country_code(self, df):
        df = df.copy()
        df["country_code"] = df["GEO_ID"].str[9:11]
        return df

    def _drop_extra_cols(self, df):
        return df[["#YR", "country_code"] + age_cols]

    def _drop_na_rows(self, df):
        return df.dropna(subset=age_cols, how="all")

    def _convert_wide_to_long(self, df):
        df["id"] = df.index
        return pd.wide_to_long(
            df,
            stubnames=["BIRTHS", "ASFR"],
            i=["#YR", "country_code", "id"],
            j="age_range",
            sep="",
            suffix=r"\d+_\d+",
        ).reset_index()

    def _hyphenate_age_range(self, df):
        df["age_range"] = df["age_range"].str.replace("_", "-")
        return df

    def _rename_cols(self, df):
        return df.rename(
            columns={"#YR": "year", "BIRTHS": "births", "ASFR": "fertility_rate"}
        ).drop(columns=["id"])


class Loader:
    def __init__(self, cnx):
        self._cnx = cnx

    def _insert(self, df, table_name):
        df.to_sql(table_name, self._cnx, if_exists="append", index=False)
        self._cnx.commit()

    def _read_ids(self, table_name, cols):
        sql_cols = (", ").join(cols)
        qry = f"select {sql_cols} from {table_name};"
        return pd.read_sql(qry, self._cnx)

    def _join_fk(self, df, id_table, on: list):
        merged_df = df.merge(id_table, on=on, how="left")
        for col in id_table.columns:
            if "id" in col:
                id_col = col
        missing = merged_df[id_col].isna().sum()
        if missing > 0:
            raise ValueError(
                f"{missing} rows in {on} failed to match with a foreign key."
            )
        return merged_df.drop(columns=[col for col in on])


class LoadCountry(Loader):
    def load(self, df):
        table_name = "country"
        self._insert(df, table_name)
        return self._read_ids(table_name, ["country_id", "country_code"])


class LoadDemographics(Loader):
    def load(self, df, country_table):
        table_name = "demographics"
        df = self._join_fk(df, id_table=country_table, on=["country_code"])
        self._insert(df, table_name)

        # Collect demo ids cols for merging to age_demographic table
        demo_ids = self._read_ids(table_name, ["demo_id", "year", "country_id"])
        demo_ids = demo_ids.merge(country_table, on="country_id", how="left")
        return demo_ids.drop(columns=["country_id"])


class LoadAge(Loader):
    def load(self, df):
        table_name = "age"
        self._insert(df, table_name)
        return self._read_ids(table_name, ["age_id", "age_range"])


class LoadAgeDemographic(Loader):
    def load(self, df, demographics_table, age_table):
        table_name = "age_demographic"
        df = self._join_fk(df, id_table=demographics_table, on=["year", "country_code"])
        df = self._join_fk(df, id_table=age_table, on=["age_range"])
        self._insert(df, table_name)


class ETLProcessor:
    def __init__(self, cnx, data_path):
        self._cnx = cnx
        self._data_path = data_path

    def _extract_demographics(self):
        return pd.read_csv(self._data_path, delimiter="|")

    def process(self):
        print("Extract...")
        df = self._extract_demographics()
        print(f"Raw data shape: {df.shape}\n")

        print("Transform...")
        country = TransformCountry().transform(df)
        demographics = TransformDemographics().transform(df)
        age = TransformAge().transform()
        age_demographic = TransformAgeDemographic().transform(df)
        print(f"Country table shape: {country.shape}")
        print(f"Demographics table shape: {demographics.shape}")
        print(f"Age table shape: {age.shape}")
        print(f"Age_Demographic table shape: {age_demographic.shape}\n")

        print("Load...")
        country_table = LoadCountry(self._cnx).load(country)
        print("Country table complete.")
        demographics_table = LoadDemographics(self._cnx).load(
            demographics, country_table
        )
        print("Demographics table complete.")
        age_table = LoadAge(self._cnx).load(age)
        print("Age table complete.")
        LoadAgeDemographic(self._cnx).load(
            age_demographic, demographics_table, age_table
        )
        print("Age_Demographic table complete.")

        print("Complete.")
