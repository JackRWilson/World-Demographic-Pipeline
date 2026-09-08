import pandas as pd


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

        # print("Transform...")

        # print("Load...")

        print("Complete.")
