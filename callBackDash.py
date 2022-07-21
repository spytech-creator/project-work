from sre_parse import State
from dash import Dash, html, dcc,  Input, Output, State
import plotly.express as px
import pandas as pd

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

   

    dcc.Graph(
        id='bar-graph',
        #figure=fig2
    ),
])

@app.callback(
    Output('bar-graph', 'figure'),
    [State('product-dropdown', 'value'), State('city-dropdown','value'), Input('year-dropdown','value')]
)
def display_graph(product,city,year):
    #productdf=df1[df1["Product"] == product]#["Month Name","Purchase_Amount"]
    if product==None:
       productdf=df1[df1["Product"] == 'Google Phone'][["Month Name","Purchase_Amount"]]
       productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index().sort_values(by='Purchase_Amount').head(500)
       #print(productdf.head())
       fig=px.bar(productdf,x="Month Name",y="Purchase_Amount", title="Bar graph for the sales of Google Phone" , color="Month Name")
       return fig
    else:
    #    productdf=df1[df1["Product"].isin(product)][["Month_Name","Purchase_Amount"]]
       productdf = df1[(df1['Product'].isin(product)) & (df1['City']==(city)) & (df1['Year1']==(year))]
       productdf=productdf.groupby('Month Name').Purchase_Amount.sum().reset_index()
       #print(productdf.head())
       fig=px.bar(productdf,x="Month Name",y="Purchase_Amount", title=f"Bar graph for the sales of {product}", color="Month Name")
       return fig


if __name__ == '__main__':
    app.run_server(debug=True)
