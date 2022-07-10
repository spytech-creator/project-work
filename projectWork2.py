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

presentStore_df = pd.read_csv(presentStore_file) 

questions= ['which category is best selling and more profitable', 'which is the best selling and more profitable sub-category',
                'which is the top selling sub-category','which customer segment is more profitable','which is the most prefered ship Mode','which region is the most profitable',
                'which city has the highest number of sales']


app.layout = html.Div(children=[
    html.H1('DATA ANALYSIS FOR GLOBAL SUPERSTORE'),
     dcc.Dropdown(id='question-dropdown',

                options=[
                 {'label':i, 'value':i} for i in questions],
                 placeholder="Select a question",
                 
            )
            ,


   

    dcc.Graph(
        id='bar-graph',
        #figure=fig1
    ),
    
])

@app.callback(
    Output('bar-graph', 'figure'),
     Input('question-dropdown', 'value')
)
def display_graph(question):
    if question=='which category is best selling and more profitable':
        category_info = presentStore_df.groupby(['Category'])[['Sales', 'Profit_Margin']].sum()
        category_info1= category_info.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        #fig1 = category_info1.plot(x=category_info.Category, y=[category_info1.Profit_Margin,category_info1.Sales], kind='bar')
        fig1 = px.bar(category_info1,x=category_info1.index,y=[category_info1.Profit_Margin,category_info1.Sales], title= "Bar graph for the Best selling and more profitable Category",barmode='group')
        #fig2 = px.bar(category_info,x=category_info.index,y=category_info.Profit_Margin, title= "Bar graph for the Best selling Category",color=category_info.index)
        return fig1
       
        

    elif question=='which is the best selling and more profitable sub-category':
        subcategory1 = presentStore_df.groupby(['Sub_Category'])[['Sales', 'Profit_Margin']].sum()
        subcategory_sales = subcategory1.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        fig1 = px.bar( subcategory_sales,x=subcategory_sales.index,y=[subcategory_sales.Profit_Margin,subcategory_sales.Sales], title= "Bar graph for the Best selling and more profitable Sub-Category",barmode='group')
        #fig2 = px.bar( subcategory_profit,x=subcategory_profit.index,y=subcategory_profit.Profit_Margin, title= "Bar graph for the Most Profitable Sub-Category",color=subcategory_profit.index)
        return fig1
       



    elif question=='which is the top selling sub-category':
        #subcategory that sold most
       subcategory = presentStore_df.groupby(['Sub_Category'])[['Quantity']].sum()#.sort_values('Quantity',ascending=False)
       fig = px.bar(subcategory,x=subcategory.index,y=subcategory.Quantity, title= "Bar graph for the top selling Sub-Category",color=subcategory.index)
       return fig     


    elif question=='which customer segment is more profitable':
        segment_profit = presentStore_df.groupby(['Segment'])[['Profit_Margin']].sum()
        fig = px.bar(segment_profit,x=segment_profit.index,y=segment_profit.Profit_Margin, title= "Bar graph for the Most Profitable Segment",color=segment_profit.index)
        return fig


    elif question=='which is the most prefered ship Mode':
        shipmode=presentStore_df.groupby(['Ship_Mode'])['Sales'].sum().reset_index(name="counts")
        fig = px.bar(shipmode,x=shipmode.Ship_Mode,y=shipmode.counts, title= "Bar graph for the Most Prefered Ship mode",color=shipmode.Ship_Mode)
        return fig   


    elif question=='which region is the most profitable':  
        region_profit = presentStore_df.groupby(['Region'])['Profit_Margin'].sum().reset_index()
        fig = px.bar(region_profit,x=region_profit.Region,y=region_profit.Profit_Margin, title= "Bar graph for the Most Profitable Region",color=region_profit.Region)
        return fig          
      
        

    else:
        city_sales = presentStore_df.groupby(['City'])['Sales', 'Quantity'].sum().sort_values('Quantity',ascending=False)
        city_sales1 = city_sales[:10]
        fig = px.bar(city_sales1,x=city_sales1.index,y=city_sales1.Quantity, title= "Bar graph for the top 10 selling City",color=city_sales1.index)
        return fig
        
           

if __name__ == '__main__':
    app.run_server(debug=True)
