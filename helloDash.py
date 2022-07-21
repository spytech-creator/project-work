from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
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

pivot=df1.groupby(['City','Month Name']).Purchase_Amount.sum()
pivot = pd.DataFrame(pivot)
pivot.reset_index()

fig = px.bar(city_sales, x=city_sales.index, y=city_sales.Purchase_Amount, color=city_sales.index, barmode="group")
fig1 = px.line(city_sales)
fig2 = px.line(pivot)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.Graph(
        id='line-graph',
        figure=fig1
    ),

    dcc.Graph(
        id='pivot-graph',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
