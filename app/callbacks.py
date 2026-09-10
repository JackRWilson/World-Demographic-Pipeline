import plotly.express as px
from dash import Input, Output, callback

from data import (
    country_df,
    demo_df,
    get_filtered_countries,
    get_filtered_recession_years,
    major_recessions,
)


# Population tab - fig 1
@callback(
    Output(component_id="output-pop-bar-graph", component_property="figure"),
    Input(component_id="input-country-pop-dropdown", component_property="value"),
)
def update_pop_bar_graph(selected_countries):

    df = demo_df.merge(country_df, on="country_id", how="left")
    if selected_countries is None:
        selected_countries = "United States"

    filtered_countries = get_filtered_countries(df, selected_countries)

    return px.bar(
        filtered_countries,
        x="year",
        y="population",
        color="country_name",
        labels={"year": "Year", "population": "Population", "country_name": "Country"},
        title="Population Over Time",
    )


# Population tab - fig 3
@callback(
    Output(
        component_id="output-natinc-migration-bar-graph", component_property="figure"
    ),
    Input(component_id="input-country-migration-dropdown", component_property="value"),
)
def update_natinc_migration_bar_graph(selected_country):

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

    return px.bar(
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


# Population tab - fig 4
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


# Recession tab - fig 1
@callback(
    Output(component_id="output-rec-pop-bar-graph", component_property="figure"),
    Input(component_id="input-rec-pop-picker", component_property="value"),
)
def update_rec_pop_bar_graph(selected_recession):
    df = demo_df.groupby("year", as_index=False)["population"].sum()
    df["growth"] = df["population"].diff()

    if selected_recession is None:
        selected_recession = list(major_recessions)[2]

    filtered_years = get_filtered_recession_years(df, selected_recession)
    recession_years = major_recessions[selected_recession]
    filtered_years["period"] = filtered_years["year"].apply(
        lambda year: "Recession" if year in recession_years else "Before/After"
    )

    fig = px.bar(
        filtered_years,
        x="year",
        y="growth",
        color="period",
        labels={"year": "Year", "growth": "Population Growth", "period": "Period"},
        title=f"World Population Changes During the {selected_recession}",
    )
    fig.update_xaxes(dtick=1, tickformat="d")
    return fig


# Recession tab - fig 2
@callback(
    Output(component_id="output-us-rec-pop-bar-graph", component_property="figure"),
    Input(component_id="input-rec-pop-picker", component_property="value"),
)
def update_us_rec_pop_bar_graph(selected_recession):
    df = demo_df.merge(country_df, on="country_id", how="left")
    df = df[df["country_name"] == "United States"]
    df = df.groupby("year", as_index=False)["population"].sum()
    df["growth"] = df["population"].diff()

    if selected_recession is None:
        selected_recession = list(major_recessions)[2]

    filtered_years = get_filtered_recession_years(df, selected_recession)
    recession_years = major_recessions[selected_recession]
    filtered_years["period"] = filtered_years["year"].apply(
        lambda year: "Recession" if year in recession_years else "Before/After"
    )

    fig = px.bar(
        filtered_years,
        x="year",
        y="growth",
        color="period",
        labels={"year": "Year", "growth": "Population Growth", "period": "Period"},
        title=f"U.S. Population Changes During the {selected_recession}",
    )
    fig.update_xaxes(dtick=1, tickformat="d")
    return fig


# Recession tab - fig 3
@callback(
    Output(component_id="output-le-bar-graph", component_property="figure"),
    Input(component_id="input-rec-le-picker", component_property="value"),
    Input(component_id="input-le-metric-picker", component_property="value"),
)
def update_rec_le_bar_graph(selected_recession, selected_metric):
    df = demo_df.groupby("year", as_index=False)[
        ["le_at_birth", "female_le_at_birth", "male_le_at_birth"]
    ].mean()

    if selected_recession is None:
        selected_recession = list(major_recessions)[2]

    filtered_years = get_filtered_recession_years(df, selected_recession)
    recession_years = major_recessions[selected_recession]
    filtered_years["period"] = filtered_years["year"].apply(
        lambda year: "Recession" if year in recession_years else "Before/After"
    )

    metric_titles = {
        "le_at_birth": "Combined",
        "female_le_at_birth": "Female",
        "male_le_at_birth": "Male",
    }

    fig = px.bar(
        filtered_years,
        x="year",
        y=selected_metric,
        color="period",
        labels={"year": "Year", selected_metric: "Life Expectancy", "period": "Period"},
        title=f"{metric_titles[selected_metric]} Life Expectancy During the {selected_recession}",
    )
    fig.update_xaxes(dtick=1, tickformat="d")
    return fig


# Recession tab - fig 4
@callback(
    Output(component_id="output-rec-natinc-bar-graph", component_property="figure"),
    Input(component_id="input-rec-natinc-picker", component_property="value"),
)
def update_rec_natinc_bar_graph(selected_recession):
    df = demo_df.groupby("year", as_index=False)[
        ["yearly_births", "yearly_deaths", "natural_increase"]
    ].mean()

    if selected_recession is None:
        selected_recession = list(major_recessions)[2]

    filtered_years = get_filtered_recession_years(df, selected_recession)

    filtered_years = filtered_years.rename(
        columns={
            "yearly_births": "Births",
            "yearly_deaths": "Deaths",
            "natural_increase": "Increase",
        }
    )

    fig = px.bar(
        filtered_years,
        x="year",
        y=["Births", "Deaths", "Increase"],
        barmode="group",
        labels={
            "year": "Year",
            "value": "Count",
            "variable": "Metric",
        },
        title=f"Births & Deaths During the {selected_recession}",
    )
    fig.update_xaxes(dtick=1, tickformat="d")
    return fig


# Recession tab - fig 5
@callback(
    Output(component_id="output-rec-gr-bar-graph", component_property="figure"),
    Input(component_id="input-rec-gr-picker", component_property="value"),
    Input(component_id="input-gr-count-picker", component_property="value"),
)
def update_rec_gr_bar_graph(selected_recession, selected_count):
    df = demo_df.merge(country_df, on="country_id", how="left")
    df = df.groupby(["year", "country_name", "country_code"], as_index=False)[
        "growth_rate"
    ].mean()

    if selected_recession is None:
        selected_recession = list(major_recessions)[2]

    filtered_years = get_filtered_recession_years(
        df, selected_recession, additional_years=0
    )
    filtered_years = filtered_years.groupby(
        ["country_name", "country_code"], as_index=False
    )["growth_rate"].mean()
    filtered_years = filtered_years.rename(columns={"growth_rate": "Growth Rate"})

    ascending = "bottom" in selected_count
    n = 50 if "50" in selected_count else 10

    filtered_years = filtered_years.sort_values(
        "Growth Rate", ascending=ascending
    ).head(n)

    x_axis = "country_code" if n == 50 else "country_name"

    return px.bar(
        filtered_years,
        x=x_axis,
        y="Growth Rate",
        labels={
            "country_name": "Country",
            "country_code": "Country",
            "Growth Rate": "Average Growth Rate (%)",
        },
        hover_name="country_name",
        title=f"Population Growth Rate During the {selected_recession}",
    )
