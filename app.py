# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Import Tree Data 
df = pd.read_csv('2015_Street_Tree_Census_-_Tree_Data.csv')

# Eliminate NaNs from Target Variables
df = df[(df["steward"].notna()) & (df["health"].notna()) & (df["spc_common"].notna()) & (df["borough"].notna())]

app = dash.Dash()

app.layout = html.Div([
    html.Div([html.H1("2015 N.Y.C. Tree Health")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div(
        [html.Div(dcc.Dropdown(id="select-borough", options=[{'label': i.title(), 'value': i} for i in pd.unique(df['borough'])],
                               value='Brooklyn', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "33%"}),
         html.Div(dcc.Dropdown(id="select-spc", options=[{'label': i.title(), 'value': i} for i in pd.unique(df['spc_common'])],
                               value='American elm', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "33%"}),
         ], className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
                                    "margin-right": "auto", "width": "80%"}),
    html.Div(
	[dcc.Graph(id="my-graph")])
], className = "container")

@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-borough", "value"),
     dash.dependencies.Input("select-spc", "value")]

)

def ugdate_figure(Borough, Species):
    dat = df[(df["borough"] == Borough) & (df["spc_common"] == Species)].sort_values(by=["steward"]).sample(n = 100, random_state = (len(df["borough"] == Borough) + len(df["spc_common"] == Species)))
    trace = [go.Scatter3d(x=dat["longitude"], y=dat["latitude"], z=dat["steward"], mode='markers', marker = {'color': pd.factorize(dat['health'])[0]*2, 'opacity': 0.8}, hovertemplate = dat['health'])]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title=f"Borough - Species<br>{Borough.title(), Species.title()}",
		scene={"aspectmode": "cube", "xaxis": {"title": "Longitude", },
                       "yaxis": {"title": "Latitude", },
                       "zaxis": {"title": "Number of Stewards", }})
		}

if __name__ == '__main__':
    app.run_server(debug=True)
            