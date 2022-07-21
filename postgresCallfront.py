#from sre_parse import State
from dash import Dash, html, dcc,  Input, Output, State
from matplotlib.pyplot import text
import plotly.express as px
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import plotly.graph_objs as go


app = Dash(__name__)

conn =create_engine('postgresql+psycopg2://postgres:rigor5878.@127.0.0.1:5432/dvdrental')
# catdf=pd.read_sql_query("select * from public.vw_distinct_film_category", conn)

# citydf=pd.read_sql_query("select * from public.vw_distinct_city", conn)

# monthdf=pd.read_sql_query("select * from public.vw_get_payment_month", conn)

# salesdf=pd.read_sql_query("select * from public.sales_by_film_category", conn)

# titledf=pd.read_sql_query("select * from public.vw_top_n_sales", conn)



sql1 = "select * from public.vw_top_n_sales"
salesdf1 = pd.read_sql_query(sql1, conn)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash-Postgres Demo'),


    dcc.Input(id="value_input",
              placeholder='Enter a value...',
              type='number',

              ),


    dcc.Graph(
        id='bar-graph',
        # figure=fig
    )
])


@app.callback(
    Output("bar-graph", "figure"),
    Input("value_input", "value")

)
def display_graph(value_input):

    totalSales = salesdf1.head(value_input)

    fig = px.bar(totalSales, x=totalSales["title"],
                 y="total_sales", title="Bargraph for total sales", color=totalSales["title"])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
