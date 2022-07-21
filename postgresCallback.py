#from sre_parse import State
from dash import Dash, html, dcc,  Input, Output, State
from matplotlib.pyplot import text
import plotly.express as px
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import plotly.graph_objs as go

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df1=pd.read_csv("C:\\data-analytics\\three_year_sales.csv")
# print(df1.head())
#print(df1.info())
city_sales=df1.groupby('City').Purchase_Amount.sum()#.sort_values(ascending=False)
city_sales=pd.DataFrame(city_sales)
city_sales.reset_index()
#print(city_sales.index)

#total sales per city
#pivot = df1.pivot_table(index=['City'],values=['Purchase_Amount'], aggfunc='sum')
#pivot

# pivot=df1.groupby(['City','Month Name']).Purchase_Amount.sum()
# pivot = pd.DataFrame(pivot)
# pivot.reset_index()

# fig = px.bar(city_sales, x=city_sales.index, y=city_sales.Purchase_Amount, color=city_sales.index, barmode="group")
# fig1 = px.line(city_sales)
# fig2 = px.line(pivot)
print("####### columns ######")
print(df1.columns)

app.layout = html.Div(children=[
    html.H1('Hello Dash---------'),
     dcc.Dropdown(id='product-dropdown',
                options=[
                 {'label':i, 'value':i} for i in df1['Product'].unique()],
                 placeholder="Select a product",
                 multi=True
            )
            ,

            dcc.Dropdown(id='city-dropdown',
                options=[
                 {'label':i, 'value':i} for i in df1['City'].unique()],
                 placeholder="Select a city",
                #  multi=True
            )
            ,

             dcc.Dropdown(id='year-dropdown',
                options=[
                 {'label':i, 'value':i} for i in df1['Year1'].unique()],
                 placeholder="Select a year",
                #  multi=True
            )
            ,

            html.Div([
        html.Div([
            html.P('Select Chart Type', className = 'fix_label', style = {'color': 'black'}),
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           options = [
                                      {'label': 'Line chart', 'value': 'line'},
                                      {'label': 'Vertical bar chart', 'value': 'vertical'}],
                           value = 'line',
                           style = {'text-align': 'center', 'color': 'black'}, className = 'dcc_compon'),

            # dcc.Graph(id = 'multi_chart',
            #           config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 six columns"),

    ], className = "row flex-display"),

   

    dcc.Graph(
        id='multi-graph',
        #figure=fig2
    ),
])

@app.callback(
    Output('multi-graph', 'figure'),
    [State('product-dropdown', 'value'), State('city-dropdown','value'), Input('year-dropdown','value'), Input('radio_items', 'value')]
)
def display_graph(product,city,year,radio_items):
    #global productdf
    if product==None and radio_items=='line':
       productdf=df1[df1["Product"] == 'Google Phone'][["Month Name","Purchase_Amount"]]
       productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index().sort_values(by='Purchase_Amount').head(500)
       #print(productdf.head())
       fig = px.line(productdf,x="Month Name",y="Purchase_Amount", title= "Line graph for the sales of Google Phone")
       return fig
        

    elif product ==None and radio_items=='vertical':
       productdf=df1[df1["Product"] == 'Google Phone'][["Month Name","Purchase_Amount"]]
       productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index().sort_values(by='Purchase_Amount').head(500)
       #print(productdf.head())
       fig = px.bar(productdf,x="Month Name",y="Purchase_Amount", title="Bar graph for the sales of Google Phone" , color="Month Name")
       return fig



    elif product==(product) and radio_items=='line':        
       productdf = df1[(df1['Product'].isin(product)) & (df1['City']==(city)) & (df1['Year1']==(year))]
       productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index()
       #print(productdf.head())
       fig = px.line(productdf,x="Month Name",y="Purchase_Amount", title= f"Line graph for the sales of {product} at {city} in {year}")
       return fig 
        

    else:
        productdf = df1[(df1['Product'].isin(product)) & (df1['City']==(city)) & (df1['Year1']==(year))]
        productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index()
        fig = px.bar(productdf,x="Month Name",y="Purchase_Amount", title= f"Bar graph for the sales of {product} at {city} in {year}" , color="Month Name")
        return fig
           

if __name__ == '__main__':
    app.run_server(debug=True)
