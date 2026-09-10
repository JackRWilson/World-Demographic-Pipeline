import os

import callbacks  # noqa: F401
from dash import Dash, dash_table, dcc, html
from graphs import pop_natinc_scatter, sum_pop_bar_graph
from inputs import (
    country_migration_dropdown,
    country_pop_dropdown,
    country_rate_dropdown,
    gr_count_picker,
    gr_recession_picker,
    le_metric_picker,
    le_recession_picker,
    natinc_recession_picker,
    pop_recession_picker,
)

from data import age_demo_df, age_df, country_df, demo_df, major_recessions

app = Dash(__name__)
server = app.server

data_table_settings = {
    "page_size": 5,
    "sort_action": "native",
    "style_table": {"overflowX": "auto"},
    "style_cell": {
        "maxWidth": "100px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "fontFamily": "Helvetica",
        "fontSize": "14px",
    },
    "style_header": {
        "backgroundColor": "#E4E4E4",
        "fontWeight": "bold",
        "fontFamily": "Helvetica",
        "fontSize": "15px",
    },
    "style_data_conditional": [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#E4E4E4",
        },
        {
            "if": {"row_index": "even"},
            "backgroundColor": "white",
        },
    ],
}


def render_table(table, cols, desc, df):
    return html.Section(
        [
            html.Div(
                [
                    html.H3(f"{table} Table", style={"margin": "0"}),
                    html.P(
                        f" - {cols}",
                        style={"margin": "0", "marginLeft": "8px"},
                    ),
                ],
                style={"display": "flex", "alignItems": "baseline"},
            ),
            html.P(desc),
            dash_table.DataTable(data=df.to_dict("records"), **data_table_settings),
        ]
    )


data_tab = dcc.Tab(
    label="Data",
    children=[
        html.Section(
            [
                html.H2("Raw Data"),
                html.Section(
                    [
                        html.A(
                            "International Database: World Population Estimates and Projections",
                            href="https://www.census.gov/programs-surveys/international-programs/about/idb.html",
                        )
                    ]
                ),
                html.H2("Tables"),
                html.Section(
                    [
                        render_table(
                            table="Country",
                            cols="country_id, country_code, country_name, area_km2",
                            desc="This table shows basic identifying info for each country.",
                            df=country_df,
                        ),
                        render_table(
                            table="Age",
                            cols="age_id, age_range",
                            desc="This age ranges with their IDs for joining with other tables.",
                            df=age_df,
                        ),
                        render_table(
                            table="Demographics",
                            cols="demo_id, year, growth_rate, population, yearly_births, yearly_deaths, natural_increase, net_migrants, net_migration_rate, rate_natural_increase, le_at_birth, female_le_at_birth, male_le_at_birth, country_id",
                            desc="This table shows all basic demographic info by year and country.",
                            df=demo_df,
                        ),
                        render_table(
                            table="Age_Demographic",
                            cols="age_demographic_id, demo_id, age_id, births, fertility_rate",
                            desc="This table combines demographic info with age range info.",
                            df=age_demo_df,
                        ),
                    ]
                ),
            ]
        )
    ],
)

pop_tab = dcc.Tab(
    label="Population Analysis",
    children=[
        html.Section(
            [
                html.H2("Question"),
                html.P(
                    "Are population increases due more to immigration or natural increase?"
                ),
                html.Br(),
                html.H2("Figure 1"),
                html.H4("Country selector:"),
                country_pop_dropdown(),
                dcc.Graph(id="output-pop-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 2"),
                dcc.Graph(figure=sum_pop_bar_graph()),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 3"),
                html.H4("Country selector:"),
                country_migration_dropdown(),
                dcc.Graph(id="output-natinc-migration-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 4"),
                html.H4("Country selector:"),
                country_rate_dropdown(),
                dcc.Graph(id="output-natinc-migration-rate-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 5"),
                dcc.Graph(figure=pop_natinc_scatter()),
                html.P("Describe trend"),
                html.Br(),
            ]
        )
    ],
)


recession_tab = dcc.Tab(
    label="Recession Analysis",
    children=[
        html.Section(
            [
                html.H2("Question"),
                html.P(
                    "How does Covid / Recession effect population, birth rates, life expectancy?"
                ),
                html.H4("Major Recessions"),
                *[
                    html.P(
                        f"{name}: {years[0]}{f'-{years[-1]}' if len(years) > 1 else ''}"
                    )
                    for name, years in major_recessions.items()
                ],
                html.Br(),
                html.H2("Figure 1 & 2"),
                html.H4("Recession selector:"),
                pop_recession_picker(),
                dcc.Graph(id="output-rec-pop-bar-graph"),
                html.P("Describe trend"),
                dcc.Graph(id="output-us-rec-pop-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 3"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Recession selector:"),
                                le_recession_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                        html.Div(
                            [
                                html.H4("Metric selector:"),
                                le_metric_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                    ],
                    style={"display": "flex", "gap": "20px"},
                ),
                dcc.Graph(id="output-le-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 4"),
                html.H4("Recession selector:"),
                natinc_recession_picker(),
                dcc.Graph(id="output-rec-natinc-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
                html.H2("Figure 5"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Recession selector:"),
                                gr_recession_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                        html.Div(
                            [
                                html.H4("Count selector:"),
                                gr_count_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                    ],
                    style={"display": "flex", "gap": "20px"},
                ),
                dcc.Graph(id="output-rec-gr-bar-graph"),
                html.P("Describe trend"),
                html.Br(),
            ]
        )
    ],
)

app.layout = html.Div(
    [
        html.Section(
            [html.H1("World Demographic Data Analysis")],
            style={"fontFamily": "Helvetica", "textAlign": "center"},
        ),
        html.Section(dcc.Tabs([recession_tab]), style={"fontFamily": "Helvetica"}),
    ],
    style={"paddingLeft": "40px", "paddingRight": "40px"},
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8050")),
        debug=os.environ.get("DASH_DEBUG", "false").lower() == "true",
    )
