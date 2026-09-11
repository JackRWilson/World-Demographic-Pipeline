from dash import dcc

from data import country_df, major_recessions


# Population tab - fig 1
def country_pop_dropdown():
    return dcc.Dropdown(
        [
            {"label": name, "value": name}
            for name in country_df["country_name"].unique()
        ],
        value=["United States", "Pakistan", "Nigeria", "Japan", "United Kingdom"],
        id="input-country-pop-dropdown",
        multi=True,
        placeholder="Select Countries",
        style={"width": "250px"},
    )


# Population tab - fig 3
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


# Population tab - fig 4
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


# Pop tab - fig 6
def corr_matrix_mode_picker():
    return dcc.RadioItems(
        id="input-corr-matrix-mode-picker",
        options=[
            {"label": "By Country", "value": "country_name"},
            {"label": "By Continent", "value": "continent"},
        ],
        value="continent",
        inline=True,
    )


# Pop tab - fig 6
def corr_matrix_value_picker():
    return dcc.Dropdown(id="input-corr-matrix-value-picker", value="North America")


# Recession tab - fig 1 & 2
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


# Recession tab - fig 3
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


# Recession tab - fig 3
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


# Recession tab - fig 4
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


# Recession tab - fig 5 & 6
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


# Recession tab - fig 5
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


# Birth age tab - fig 1
def country_fr_dropdown():
    return dcc.Dropdown(
        [
            {"label": name, "value": name}
            for name in country_df["country_name"].unique()
        ],
        value=["China"],
        id="input-country-fr-dropdown",
        placeholder="Select Country",
        style={"width": "250px"},
    )
