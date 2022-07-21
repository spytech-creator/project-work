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

sql1 = "select * from public.vw_top_paying_customers"
topdf1 = pd.read_sql_query(sql1, conn)

sql2 = '''SELECT s.store_id,
	      EXTRACT(ISOYEAR FROM r.rental_date) AS rental_year,
	      EXTRACT(MONTH FROM r.rental_date) AS rental_month,
	      COUNT(r.rental_id) AS count_rentals
     FROM rental r
     JOIN staff
    USING (staff_id)
     JOIN store s
    USING (store_id)
 GROUP BY 1, 2, 3
 ORDER BY 1, 2, 3;'''

storedf = pd.read_sql_query(sql2, conn)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash-Postgres Demo'),


    dcc.Input(id="top",
              placeholder='Enter a value...',
              type='number',

              ),


    dcc.Graph(
        id='bar-graph',
        # figure=fig
    ),

     dcc.Graph(
        id='example-graph',
        # figure=fig
    )
])


@app.callback(
    Output("bar-graph", "figure"),
    Input("top", "value")

)
def display_graph(top):

    topCustomers = topdf1.head(top)

    fig = px.bar(topCustomers, x=topCustomers["customer_name"],
                 y="total_payment", title="Bargraph for customer purchases", color=topCustomers["payment_month"], barmode='group')
    return fig

# @app.callback(
#     Output("example-graph", "figure")

# )    

def display_graph2():
    fig = px.bar(storedf, x=storedf["rental_month"],
                 y="count_rentals", title="Bargraph for rentals in two stores", color=storedf["rental_year"], barmode='group')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
