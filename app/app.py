import os

import callbacks  # noqa: F401
from dash import Dash, dash_table, dcc, html
from graphs import (
    avg_age_childbirth_graph,
    birth_percent_bar_graph,
    fr_combined_line_graph,
    pop_natinc_scatter,
    sum_pop_bar_graph,
)
from inputs import (
    corr_matrix_mode_picker,
    corr_matrix_value_picker,
    country_fr_dropdown,
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
        "backgroundColor": "#BDBDBD",
        "fontWeight": "bold",
        "fontFamily": "Helvetica",
        "fontSize": "15px",
    },
    "style_data_conditional": [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#D3D3D3",
        },
        {
            "if": {"row_index": "even"},
            "backgroundColor": "white",
        },
    ],
}

figure_style = {"padding": "16px 8px", "backgroundColor": "#777777", "color": "white"}
tab_style = {"backgroundColor": "#777777", "color": "white", "fontSize": "20px"}
tab_selected_style = {"backgroundColor": "#6082B6", "color": "white"}


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
                html.Br(),
                html.H2("Raw Data", style=figure_style),
                html.Section(
                    [
                        html.A(
                            "International Database: World Population Estimates and Projections",
                            href="https://www.census.gov/programs-surveys/international-programs/about/idb.html",
                        )
                    ]
                ),
                html.Br(),
                html.H2("Tables", style=figure_style),
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
                            desc="This table has age ranges with their IDs for joining with other tables.",
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
    style=tab_style,
    selected_style=tab_selected_style,
)

pop_tab = dcc.Tab(
    label="Population Analysis",
    children=[
        html.Section(
            [
                html.Br(),
                html.H2("Question", style=figure_style),
                html.P(
                    "Are population increases due more to immigration or natural increase?"
                ),
                html.P(
                    [
                        html.B("Short Answer: "),
                        """Overall increases are due to natural increase, but 
                       different countries see differing levels of net migration and natural
                       increase.""",
                    ]
                ),
                html.Br(),
                html.H2("Figure 1", style=figure_style),
                html.H4("Country selector:"),
                country_pop_dropdown(),
                dcc.Graph(id="output-pop-bar-graph"),
                html.P(
                    """We can see from this that many countries' populations are increasing 
                    over time, and is forecasted to keep growing."""
                ),
                html.Br(),
                html.H2("Figure 2", style=figure_style),
                dcc.Graph(figure=sum_pop_bar_graph()),
                html.P(
                    """Overall world population has also been increasing and is forecasted to 
                    continue, with total population into 8 billion in 2025."""
                ),
                html.Br(),
                html.H2("Figure 3", style=figure_style),
                html.H4("Country selector:"),
                country_migration_dropdown(),
                dcc.Graph(id="output-natinc-migration-bar-graph"),
                html.P(
                    """This graph shows the number of people that have migrated to/from the 
                    selected country, versus the number of people that were naturally born in 
                    that country. This is very country dependent. The United States sees lots 
                    of population growth from migration, but Zimbabwe sees lots of its population 
                    growth from births, with a decline from migration."""
                ),
                html.Br(),
                html.H2("Figure 4", style=figure_style),
                html.H4("Country selector:"),
                country_rate_dropdown(),
                dcc.Graph(id="output-natinc-migration-rate-graph"),
                html.P(
                    """This graph shows the same information as the previous one, but is 
                       standardized across all countries. We can see from this that world 
                       population increases are due to natural births, which makes sense because 
                       when everything is aggregated migration doesn't change the overall 
                       population."""
                ),
                html.Br(),
                html.H2("Figure 5", style=figure_style),
                dcc.Graph(figure=pop_natinc_scatter()),
                html.P(
                    """We can see from this scatter plot that there is little correlation
                       between migrant versus natural population increases. It is interesting
                       to see that China (overall) has a negative average natural increase and
                       negative average net migrants. Where India has had lots of people migrating
                       away but has lots of births."""
                ),
                html.Br(),
                html.H2("Figure 6", style=figure_style),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Mode selector:"),
                                corr_matrix_mode_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                        html.Div(
                            [
                                html.H4("Value selector:"),
                                corr_matrix_value_picker(),
                            ],
                            style={"flex": "1"},
                        ),
                    ],
                    style={"display": "flex", "gap": "20px"},
                ),
                dcc.Graph(id="output-pop-natinc-corr-matrix"),
                html.P(
                    """We can see from this correlation matrix that there is little correlation
                       between natural increase and net migration, which supports our other
                       findings. North America has the largest correlation magnitude at -0.37. 
                       This means that across the years, when net natural increase tends to be 
                       higher, net migration tends to be somewhat lower (and vice versa), but the 
                       relationship isn't very strong."""
                ),
                html.Br(),
            ]
        )
    ],
    style=tab_style,
    selected_style=tab_selected_style,
)


recession_tab = dcc.Tab(
    label="Recession Analysis",
    children=[
        html.Section(
            [
                html.Br(),
                html.H2("Question", style=figure_style),
                html.P(
                    "How does Covid / Recession affect population, birth rates, life expectancy?"
                ),
                html.P(
                    [
                        html.B("Short Answer: "),
                        """Population still grows during recessions, albeit at a 
                       slightly slower rate. Births and deaths also seem to remain fairly 
                       constant, and there is almost no change in life expectancy during a 
                       recession.""",
                    ]
                ),
                html.H4("Major Recessions"),
                *[
                    html.P(
                        f"{name}: {years[0]}{f'-{years[-1]}' if len(years) > 1 else ''}"
                    )
                    for name, years in major_recessions.items()
                ],
                html.Br(),
                html.H2("Figure 1 & 2", style=figure_style),
                html.H4("Recession selector:"),
                pop_recession_picker(),
                dcc.Graph(id="output-rec-pop-bar-graph"),
                html.P(
                    """Overall population seems to still grow during recessions, just at a 
                       steady or slower rate. The COVID Recession had the most dramatic decreases
                       in population growth during and following the recession."""
                ),
                dcc.Graph(id="output-us-rec-pop-bar-graph"),
                html.P(
                    """This trend seems to hold in the U.S. apart from the COVID Recession
                       again. The U.S. saw a massive decrease in growth with an increase of 
                       only ~500,000 post pandemic."""
                ),
                html.Br(),
                html.H2("Figure 3", style=figure_style),
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
                html.P(
                    """Life expectancy remains steady even through recessions and across
                       genders. It's notable that across all recessions analyzed, females
                       always had a higher life expectancy than males, though this likely has
                       nothing to do with the recession itself."""
                ),
                html.Br(),
                html.H2("Figure 4", style=figure_style),
                html.H4("Recession selector:"),
                natinc_recession_picker(),
                dcc.Graph(id="output-rec-natinc-bar-graph"),
                html.P(
                    """This graph shows the same +3 years -3 years time window around the
                       recession but is clustered into total births/deaths/increase. This lets
                       us see how each variable was impacted by the recession. The Great 
                       Recession had little impact on any of these metrics, while COVID and the
                       1981-1982 Recessions saw a slight dip in births. Most other variable 
                       remained constant."""
                ),
                html.Br(),
                html.H2("Figure 5 & 6", style=figure_style),
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
                html.P(
                    """We can see that a recessions impact on population growth rate is 
                       very country specific. Some countries will still have a high growth 
                       rate, while others will be very low. This is just due to the nature of 
                       how recessions impact a worldwide ecosystem."""
                ),
                dcc.Graph(id="output-rec-gr-map"),
                html.P(
                    """This map shows the same data from before but across the whole globe
                       and is a better visualization of regional impact. The COVID Recession 
                       impacted the whole globe, but many of the countries in Africa still had
                       a high population growth, showing it may not have impacted them as much."""
                ),
                html.Br(),
            ]
        )
    ],
    style=tab_style,
    selected_style=tab_selected_style,
)

birth_age_tab = dcc.Tab(
    label="Birth Age Analysis",
    children=[
        html.Section(
            [
                html.Br(),
                html.H2("Question", style=figure_style),
                html.P(
                    "How has the age at which women have children changed over time?"
                ),
                html.P(
                    [
                        html.B("Short Answer: "),
                        """Women have started having children later in life. This
                       could be due to many factors (career, birth control options, overall 
                       culture/value changes).""",
                    ]
                ),
                html.Br(),
                html.H2("Figure 1 & 2", style=figure_style),
                country_fr_dropdown(),
                dcc.Graph(id="output-fr-line-graph"),
                html.P(
                    """This graph shows the fertility rate of women in each age group over 
                       time. In China in 1990, women ages 20-24 used to have the highest fertility
                       rate, but over time women have joined the workforce instead of staying at 
                       home, pushing family life off to a later age."""
                ),
                dcc.Graph(figure=fr_combined_line_graph()),
                html.P(
                    """The trend seen in China seems to be reflected across the globe. Women
                       15-19, 40-44, and 45-49 have the lowest fertility rates, and have stayed
                       consistent over time. Women 20-24 saw a rise in rates in 1980 before 
                       dropping back down. Women ages 25-34 have the highest fertility rate."""
                ),
                html.Br(),
                html.H2("Figure 3", style=figure_style),
                dcc.Graph(figure=birth_percent_bar_graph()),
                html.P(
                    """This chart shows the percentage of total global births each age group
                       had. Similarly to before, women used to have children earlier, but are
                       now pushing it back to pursue a career or because more birth control 
                       options are available."""
                ),
                html.Br(),
                html.H2("Figure 4", style=figure_style),
                dcc.Graph(figure=avg_age_childbirth_graph()),
                html.P(
                    """We can see in this graph that the average age women gave birth at was 
                       fairly young, but since 2000 has been increasing, supporting our other 
                       findings."""
                ),
                html.Br(),
            ]
        )
    ],
    style=tab_style,
    selected_style=tab_selected_style,
)

app.layout = html.Div(
    [
        html.Br(),
        html.Section(
            [html.H1("World Demographic Data Analysis")],
            style={"fontFamily": "Helvetica", "textAlign": "center"},
        ),
        html.Br(),
        html.Section(
            dcc.Tabs([data_tab, pop_tab, recession_tab, birth_age_tab]),
            style={"fontFamily": "Helvetica"},
        ),
    ],
    style={"paddingLeft": "40px", "paddingRight": "40px"},
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8050")),
        debug=os.environ.get("DASH_DEBUG", "false").lower() == "true",
    )
