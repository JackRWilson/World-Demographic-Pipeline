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
