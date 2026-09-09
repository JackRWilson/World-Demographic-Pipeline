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

    def _rename_cols(self, df):
        return df.rename(
            columns={"#YR": "year", "BIRTHS": "births", "ASFR": "fertility_rate"}
        ).drop(columns=["id"])


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
        print(age_demographic.head())
        print(f"Country table shape: {country.shape}")
        print(f"Demographics table shape: {demographics.shape}")
        print(f"Age table shape: {age.shape}")
        print(f"Age_Demographic table shape: {age_demographic.shape}")

        # print("Load...")

        print("Complete.")
