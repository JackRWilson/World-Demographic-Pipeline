from dash import dcc

from data import country_df, major_recessions


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


def pop_recession_picker():
    return dcc.RadioItems(
        options=[{"label": name, "value": name} for name in major_recessions],
        value=list(major_recessions)[2],
        id="input-rec-pop-picker",
        inline=True,
        labelStyle={
            "display": "inline-block",
            "cursor": "pointer",
        },
    )


def le_recession_picker():
    return dcc.RadioItems(
        options=[{"label": name, "value": name} for name in major_recessions],
        value=list(major_recessions)[2],
        id="input-rec-le-picker",
        inline=True,
        labelStyle={
            "display": "inline-block",
            "cursor": "pointer",
        },
    )


def natinc_recession_picker():
    return dcc.RadioItems(
        options=[{"label": name, "value": name} for name in major_recessions],
        value=list(major_recessions)[2],
        id="input-rec-natinc-picker",
        inline=True,
        labelStyle={
            "display": "inline-block",
            "cursor": "pointer",
        },
    )


def gr_recession_picker():
    return dcc.RadioItems(
        options=[{"label": name, "value": name} for name in major_recessions],
        value=list(major_recessions)[2],
        id="input-rec-gr-picker",
        inline=True,
        labelStyle={
            "display": "inline-block",
            "cursor": "pointer",
        },
    )


def le_metric_picker():
    return dcc.RadioItems(
        id="input-le-metric-picker",
        options=[
            {"label": "All", "value": "le_at_birth"},
            {"label": "Female", "value": "female_le_at_birth"},
            {"label": "Male", "value": "male_le_at_birth"},
        ],
        value="le_at_birth",
        inline=True,
        labelStyle={
            "display": "inline-block",
            "cursor": "pointer",
        },
    )

def gr_count_picker():
    return dcc.RadioItems(
        id="input-gr-count-picker",
        options=[
            {"label": "Top 10", "value": "top10"},
            {"label": "Top 50", "value": "top50"},
            {"label": "Bottom 10", "value": "bottom10"},
            {"label": "Bottom 50", "value": "bottom50"},
        ],
        value="top10",
        inline=True,
    )