import plotly.express as px
from dash import Input, Output, callback

from data import country_df, demo_df, get_filtered_countries


@callback(
    Output(component_id="output-pop-line-graph", component_property="figure"),
    Input(component_id="input-country-pop-dropdown", component_property="value"),
)
def update_pop_line_graph(selected_countries):

    df = demo_df.merge(country_df, on="country_id", how="left")
    if selected_countries is None:
        selected_countries = "United States"

    filtered_countries = get_filtered_countries(df, selected_countries)

    return px.line(
        filtered_countries,
        x="year",
        y="population",
        color="country_name",
        labels={"year": "Year", "population": "Population", "country_name": "Country"},
        title="Population Over Time",
    )


@callback(
    Output(
        component_id="output-natinc-migration-line-graph", component_property="figure"
    ),
    Input(component_id="input-country-migration-dropdown", component_property="value"),
)
def update_natinc_migration_line_graph(selected_country):

    df = demo_df.merge(country_df, on="country_id", how="left")
    if selected_country is None:
        selected_country = "United States"

    filtered_countries = get_filtered_countries(df, selected_country)

    df = filtered_countries.rename(
        columns={
            "net_migrants": "Net Migrants",
            "natural_increase": "Natural Increase",
        }
    )

    return px.line(
        df,
        x="year",
        y=["Natural Increase", "Net Migrants"],
        labels={
            "year": "Year",
            "value": "Change in Population",
            "variable": "Metric",
        },
        title="Natural Increase vs Migration Increase",
    )


@callback(
    Output(
        component_id="output-natinc-migration-rate-graph", component_property="figure"
    ),
    Input(component_id="input-country-rate-dropdown", component_property="value"),
)
def update_sum_standardized_natinc_vs_migration_graph(country):
    df = demo_df.merge(country_df, on="country_id", how="left")
    if country is None:
        country = [c for c in country_df["country_name"].unique()]

    df = get_filtered_countries(df, country)
    df["rate_natural_increase_per_1000"] = df["rate_natural_increase"] * 10
    df = df.groupby("year", as_index=False)[
        ["net_migration_rate", "rate_natural_increase_per_1000"]
    ].sum()

    df = df.rename(
        columns={
            "net_migration_rate": "Net Migration Rate",
            "rate_natural_increase_per_1000": "Natural Increase Rate",
        }
    )

    return px.bar(
        df,
        x="year",
        y=["Net Migration Rate", "Natural Increase Rate"],
        labels={
            "year": "Year",
            "value": "Rate per 1000 People",
            "variable": "Metric",
        },
        title="Total Net Migration and Natural Increase Rates Over Time",
    )
