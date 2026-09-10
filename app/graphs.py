import plotly.express as px

from data import country_df, demo_df


def sum_pop_bar_graph():
    df = demo_df.merge(country_df, on="country_id", how="left")
    df = df.groupby("year", as_index=False)["population"].sum()
    return px.bar(
        df,
        x="year",
        y="population",
        labels={"year": "Year", "population": "Population"},
        title="Total Population Over Time",
    )


def pop_natinc_scatter():
    df = demo_df.merge(country_df, on="country_id", how="left")
    df = df.groupby("country_name", as_index=False)[
        ["natural_increase", "net_migrants"]
    ].mean()
    return px.scatter(
        df,
        x="natural_increase",
        y="net_migrants",
        color="country_name",
        labels={
            "natural_increase": "Average Natural Increase",
            "net_migrants": "Average Net Migrants",
            "country_name": "Country Name",
        },
        title="Correlation Between Natural & Migrant Increase",
    )
