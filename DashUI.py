import pickle
import pandas as pd
import numpy as np
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = "Sentiment Analysis with Insights"
#project_name = None


def open_browser():
    return webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    global df, dfs
    
    df = pd.read_csv("balanced_reviews.csv")
    dfs = pd.read_csv("scrappedReviews.csv")   
    
    
    with open("pickle_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    with open("feature.pkl", 'rb') as voc:
        vocab = pickle.load(voc)
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    global df
    df = df.dropna()
    df = df[df['overall'] != 3]
    df['Positivity'] = np.where(df['overall'] > 3, 1, 0)   
    labels = ['Positive Reviews', 'Negative Reviews']
    values = [len(df[df.Positivity == 1]), len(df[df.Positivity == 0])]
    colors = ['#00cd00', '#d80000', '#a6a6a6']
    main_layout = dbc.Container(
        dbc.Jumbotron(
                [
                    #html.H1(id = 'heading', children = project_name, className = 'display-3 mb-4'),
                    html.H1(id='heading1', children='Sentiment Analysis With Insights',
                            className='display-3 mb-4', style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '50px', 'color': 'black','background-color':'aqua','border-style':'outset','display':'inline-block','width':'100%'}),               
                    html.P(id='heading5', children='Piechart Of Reviews',
                            className='display-3 mb-4', style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '30px', 'color': 'black','backgroundColor':'pink','border-style':'outset','display':'inline-block','width':'100%'}),
                     dbc.Container(
                        dcc.Loading(
                            dcc.Graph(
                                figure={'data': [go.Pie(labels=labels, values=values, textinfo='value', marker=dict(colors=colors, line=dict(color='#000000', width=2)))],
                                        'layout': go.Layout(height=500, width=900, autosize=False)
                                        }

                            )
                        ),
                        className = 'd-flex justify-content-center'
                    ),
                    #dbc.Button("Submit", color="dark", className="mb-3", id = 'button', style = {'width': '100px'}),
                    #html.Div(id = 'result'),
                    dbc.Container([
                     #dcc.col([
                    html.Div([html.H2('Word Cloud',style={"margin":"15px",'backgroundColor':'pink','border-style':'outset','display':'inline-block','width':'100%'}),
                    dbc.Button("ALL Words",id="allbt",outline=True,color="info", className="mr-1",n_clicks_timestamp=0,style={'margin':'auto',}),
                    dbc.Button("Positve Words",id="posbt",outline=True,color="success",className="mr-1",n_clicks_timestamp=0,style={'margin':'auto',}),
                    dbc.Button("Negative Words",id="negbt",outline=True, color="danger",className="mr-1",n_clicks_timestamp=0,style={'margin':'auto',})
                     ],style={'margin':'auto'}
                   ),
                    html.Div(id='container',style={'padding':'15px'})
                    
                    ]),
                    html.Hr(),
                    html.P(id='heading2', children='Feel as you type!',
                           className=' mb-3', style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '30px', 'color': 'black','backgroundColor':'pink','border-style':'outset','display':'inline-block','width':'100%'}),
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value = 'Great looking shoes i like it', style = {'height': '150px','color': 'gray'}),
                    #dbc.Button("Submit", color="dark", className="mb-3", id = 'button', style = {'width': '100px'}),
                    #html.Div(id = 'result'),
                    html.Hr(),
                    html.P(id='heading3', children=' Etsy Scrapped Review ',
                           className=' mb-3', style={'font': 'sans-serif', 'font-weight': 'bold', 'font-size': '30px', 'color': 'black','backgroundColor':'pink','border-style':'outset','display':'inline-block','width':'100%'}),
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in dfs.reviews],
                    value = df.reviewText[0],
                    style = {'margin-bottom': '30px','color': 'black'}
                    )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                    html.Div(id = 'result'),
                    html.Div(id = 'result1')
                    ],
                        className = 'text-center'
                ),
                className = 'mt-4'
            )
    return main_layout
@app.callback(
    Output('container','children'),
    [
        Input('allbt','n_clicks_timestamp'),
        Input('posbt','n_clicks_timestamp'),
        Input('negbt','n_clicks_timestamp'),
    ]
)
def wordcloudbutton(allbt,posbt,negbt):

    if int(allbt) > int(posbt) and int(allbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('wholeword.png'))])
    elif int(posbt) > int(allbt) and int(posbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('posword.png'))
            ])
    elif int(negbt) > int(allbt) and int(negbt) > int(posbt):
       return html.Div([
           html.Img(src=app.get_asset_url('negword.png'))
           ])
    else:
        pass

@app.callback(
    Output('result', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
    State('textarea', 'value')
    ]
    )    
def update_app_ui(n_clicks, textarea):
    result_list = check_review(textarea)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative Review", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive Review", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
     State('dropdown', 'value')
     ]
    )
def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative Review", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive Review", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")
    
def main():
    global app
    global project_name
    load_model()
    open_browser()
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    print("This would be executed only after the script is closed")
    app = None
    project_name = None
if __name__ == '__main__':
    main()

