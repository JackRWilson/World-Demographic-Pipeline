from dash import dcc

from data import country_df


def country_pop_dropdown():
    return dcc.Dropdown(
        [
            {"label": name, "value": name}
            for name in country_df["country_name"].unique()
        ],
        value=["United States"],
        id="input-country-pop-dropdown",
        multi=True,
        placeholder="Select Countries",
        style={"width": "250px"},
    )


def country_migration_dropdown():
    return dcc.Dropdown(
        [
            {"label": name, "value": name}
            for name in country_df["country_name"].unique()
        ],
        value=["United States"],
        id="input-country-migration-dropdown",
        placeholder="Select Country",
        style={"width": "250px"},
    )


def country_rate_dropdown():
    return dcc.Dropdown(
        [
            {"label": name, "value": name}
            for name in country_df["country_name"].unique()
        ],
        id="input-country-rate-dropdown",
        multi=True,
        placeholder="Select Country",
        style={"width": "250px"},
    )
