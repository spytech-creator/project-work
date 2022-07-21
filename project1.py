
#from sre_parse import State
from itertools import count
from dash import Dash, html, dcc,  Input, Output, State
from matplotlib.pyplot import text
import plotly.express as px
import pandas as pd
import psycopg2 as pg
import os
from sqlalchemy import create_engine
import plotly.graph_objs as go

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
path = 'globalUsers' 
presentStore_file = os.path.join(path, 'newSuperstore.csv')

newStore_df = pd.read_csv(presentStore_file) 
#CATEGORY ANALYSIS
category_info = newStore_df.groupby(['Category'])[['Sales', 'Profit_Margin']].sum()
category_info1= category_info.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
fig = px.bar(category_info1,x=category_info1.index,y=[category_info1.Profit_Margin,category_info1.Sales], title= "Bar graph for the Best selling and more profitable Category",barmode='group')

#SUB-CATEGORY ANALYSIS
subcategory1 = newStore_df.groupby(['Sub_Category'])[['Sales', 'Profit_Margin']].sum()
subcategory_sales = subcategory1.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
fig1 = px.bar( subcategory_sales,x=subcategory_sales.index,y=[subcategory_sales.Profit_Margin,subcategory_sales.Sales], title= "Bar graph for the Best selling and more profitable Sub-Category",barmode='group')

subcategory = newStore_df.groupby(['Sub_Category'])[['Quantity']].sum()#.sort_values('Quantity',ascending=False)
fig2 = px.bar(subcategory,x=subcategory.index,y=subcategory.Quantity, title= "Bar graph for the top selling Sub-Category",color=subcategory.index)

#SEGMENT ANALYSIS
segment_profit = newStore_df.groupby(['Segment'])[['Profit_Margin']].sum()
fig3 = px.bar(segment_profit,x=segment_profit.index,y=segment_profit.Profit_Margin, title= "Bar graph for the Most Profitable Segment",color=segment_profit.index)

#SHIPMODE ANALYSIS
shipmode=newStore_df.groupby(['Ship_Mode'])['Sales'].sum().reset_index(name="counts")
fig4 = px.bar(shipmode,x=shipmode.Ship_Mode,y=shipmode.counts, title= "Bar graph for the Most Prefered Ship mode",color=shipmode.Ship_Mode)

#REGIONAL ANALYSIS
region_profit = newStore_df.groupby(['Region'])['Profit_Margin'].sum().reset_index()
fig5 = px.bar(region_profit,x=region_profit.Region,y=region_profit.Profit_Margin, title= "Bar graph for the Most Profitable Region",color=region_profit.Region)

#CITY ANALYSIS
city_sales = newStore_df.groupby(['City'])['Sales', 'Quantity'].sum().sort_values('Quantity',ascending=False)
city_sales1 = city_sales[:10]
fig6 = px.bar(city_sales1,x=city_sales1.index,y=city_sales1.Quantity, title= "Bar graph for the top 10 selling City",color=city_sales1.index)


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children="BEST SELLING AND MOST PROFITABLE CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph9',
                figure=fig
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children="BEST SELLING AND MOST PROFITABLE SUB-CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children="TOP SELLING SUB-CATEGORY", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children="MOST PROFITABLE CUSTOMER SEGMENT", style={'textAlign': 'center'}),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ], className='row'),
    html.Div([
            html.H1(children="MOST PREFERED SHIP MODE", style={'textAlign': 'center'}),


dcc.Graph(
                id='graph4',
                figure=fig4
            ),  
        ], className='six columns'),
        html.Div([
        html.H1(children="MOST PROFITABLE REGION", style={'textAlign': 'center'}),

        dcc.Graph(
            id='graph5',
            figure=fig5
        ),  
    ], className='row'),
    html.Div([
            html.H1(children="HIGHEST SELLING CITIES", style={'textAlign': 'center'}),

            dcc.Graph(
                id='graph6',
                figure=fig6
            ),  
        ], className='six columns'),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)