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
catdf=pd.read_sql_query("select * from public.vw_distinct_film_category", conn)

citydf=pd.read_sql_query("select * from public.vw_distinct_city", conn)

monthdf=pd.read_sql_query("select * from public.vw_get_payment_month", conn)

salesdf=pd.read_sql_query("select * from public.sales_by_film_category", conn)

titledf=pd.read_sql_query("select * from public.vw_top_n_sales", conn)



app.layout = html.Div(children=[
    html.H1('Hello Dash-PostgresSQL Demo'),
     dcc.Dropdown(id='category-dropdown',
                options=[
                 {'label':i, 'value':i} for i in catdf['name']],
                 placeholder="Select a category",
                 multi=True
            )
            ,

            dcc.Dropdown(id='city-dropdown',
                options=[
                 {'label':i, 'value':i} for i in citydf['city']],
                 placeholder="Select a city",
                #  multi=True
            )
            ,

             dcc.Dropdown(id='month-dropdown',
                options=[
                 {'label':i, 'value':i} for i in monthdf['month']],
                 placeholder="Select a month",
                #  multi=True
            )
            ,
   

    dcc.Graph(
        id='bar-graph',
        #figure=fig2
    ),
])

@app.callback(
    Output('bar-graph', 'figure'),
    [State('category-dropdown', 'value'), State('city-dropdown','value'), Input('month-dropdown','value')]
)
def display_graph(name,city,month):
    #global productdf
    if name==None:
       
       fig = px.bar(salesdf,x="category",y="total_sales", color='category',title= "Line graph for the total sales of Action movies")
       return fig
        
    else:
        sql1=f'''
        SELECT c.name AS category,
        sum(p.amount) AS total_sales,trim(to_char(p.payment_date,'MONTH')) as month,
	    ct.city
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
	    JOIN customer cus ON cus.customer_id = p.customer_id
	    JOIN address ad ON ad.address_id= cus.address_id
	    JOIN city ct ON ct.city_id=ad.city_id
        WHERE trim(to_char(payment_date,'MONTH'))=trim('{month}') 
        AND ct.city='{city}'
        GROUP BY c.name,month,ct.city
        ORDER BY (sum(p.amount)) DESC;'''
        titledf1=pd.read_sql_query(sql1, conn)
        fig = px.bar(titledf1,x="category",y="total_sales", color='category', title= f"Bar graph for the sales of {name} at {city} in {month}")
        return fig
           

if __name__ == '__main__':
    app.run_server(debug=True)
