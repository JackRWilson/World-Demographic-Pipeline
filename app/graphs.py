import plotly.express as px

from data import age_demo_df, age_df, age_midpoints, country_df, demo_df


def add_forecast_highlight(fig, year_col, color="red"):
    return fig.add_vrect(
        x0=2025,
        x1=year_col.max(),
        fillcolor=color,
        opacity=0.05,
        line_width=0,
        annotation_text="Forecast",
        annotation_position="top left",
    )


# Pop tab - fig 2
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


# Pop tab - fig 5
def pop_natinc_scatter():
    df = demo_df.merge(country_df, on="country_id", how="left")
    df = df.groupby("country_name", as_index=False)[
        ["natural_increase", "net_migrants", "population"]
    ].mean()
    return px.scatter(
        df,
        x="natural_increase",
        y="net_migrants",
        color="country_name",
        size="population",
        labels={
            "natural_increase": "Average Natural Increase",
            "net_migrants": "Average Net Migrants",
            "country_name": "Country Name",
        },
        title="Correlation Between Natural & Migrant Increase",
    )


# Birth age tab - fig 2
def fr_combined_line_graph():
    df = age_demo_df.merge(demo_df, on="demo_id", how="left")
    df = df.merge(age_df, on="age_id", how="left")
    df = df.merge(country_df, on="country_id", how="left")
    df = df[["year", "age_range", "fertility_rate"]]

    df = df.groupby(["year", "age_range"], as_index=False)["fertility_rate"].mean()

    fig = px.line(
        df,
        x="year",
        y="fertility_rate",
        color="age_range",
        labels={
            "year": "Year",
            "fertility_rate": "Fertility Rate",
            "age_range": "Age Group",
        },
        title="Fertility Rate by Age Group Over Time - All Countries",
    )
    add_forecast_highlight(fig, df["year"])
    return fig


# Birth age tab - fig 3
def birth_percent_bar_graph():
    df = age_demo_df.merge(demo_df, on="demo_id", how="left")
    df = df.merge(age_df, on="age_id", how="left")
    df = df[["year", "age_range", "births"]]

    df = df.groupby(["year", "age_range"], as_index=False)["births"].sum()
    yearly_totals = df.groupby("year", as_index=False)["births"].sum()
    yearly_totals = yearly_totals.rename(columns={"births": "total_births"})

    df = df.merge(yearly_totals, on="year", how="left")
    df["birth_percent"] = (df["births"] / df["total_births"]) * 100

    fig = px.bar(
        df,
        x="year",
        y="birth_percent",
        color="age_range",
        labels={
            "year": "Year",
            "birth_percent": "Percent of Total Births",
            "age_range": "Age Group",
        },
        title="Share of Births by Age Group Over Time",
    )
    add_forecast_highlight(fig, df["year"], color="black")
    return fig


# Birth age tab - fig 4
def avg_age_childbirth_graph():
    df = age_demo_df.merge(demo_df, on="demo_id", how="left")
    df = df.merge(age_df, on="age_id", how="left")
    df = df[["year", "age_range", "births"]]

    df = df.groupby(["year", "age_range"], as_index=False)["births"].sum()

    # Map age group to midpoint
    df["midpoint"] = df["age_range"].map(age_midpoints)

    # Avg Age = sum(midpoint * births in group) / total births
    df["weighted"] = df["midpoint"] * df["births"]
    yearly = df.groupby("year", as_index=False)[["weighted", "births"]].sum()
    yearly["avg_age"] = yearly["weighted"] / yearly["births"]

    fig = px.line(
        yearly,
        x="year",
        y="avg_age",
        line_shape="hv",
        labels={"year": "Year", "avg_age": "Average Age at Childbirth"},
        title="Average Age at Childbirth Over Time",
    )
    add_forecast_highlight(fig, yearly["year"])
    return fig
