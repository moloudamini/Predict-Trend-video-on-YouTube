#Reference: https://medium.com/ai%E8%82%A1%E4%BB%94/%E5%AD%B8%E6%9C%83%E7%94%A8%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92%E9%A0%90%E6%B8%AC%E8%82%A1%E5%83%B9-%E5%AE%8C%E6%95%B4%E6%B5%81%E7%A8%8B%E6%95%99%E5%AD%B8%E8%88%87%E5%AF%A6%E4%BD%9C-b057e7343ca4

import sys
import os
from collections import namedtuple
import pkg_resources

IS_FROZEN = hasattr(sys, '_MEIPASS')

# backup true function
_true_get_distribution = pkg_resources.get_distribution
# create small placeholder for the dash call
# _flask_compress_version = parse_version(get_distribution("flask-compress").version)
_Dist = namedtuple('_Dist', ['version'])

def _get_distribution(dist):
    if IS_FROZEN and dist == 'flask-compress':
        return _Dist('1.8.0')
    else:
        return _true_get_distribution(dist)

# monkey patch the function so it can work once frozen and pkg_resources is of
# no help
pkg_resources.get_distribution = _get_distribution

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from joblib import dump, load

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='AI Trend video prediction', style={'textAlign': 'center'}),
    html.Div(["Please select a country: ",
              dcc.Dropdown(
                 id='drp-country',
                 options=[
                    {'label': 'Canada', 'value': 'CA'},
                    {'label': 'Brazil', 'value': 'BR'},
                    {'label': 'Germany', 'value': 'DE'},
                    {'label': 'France', 'value': 'FR'},
                    {'label': 'United Kindom', 'value': 'GB'},
                    {'label': 'India', 'value': 'IN'},
                    {'label': 'Japan', 'value': 'JP'},
                    {'label': 'Korea', 'value': 'KR'},
                    {'label': 'Mexico', 'value': 'MX'},
                    {'label': 'Russia', 'value': 'RU'},
                    {'label': 'United States', 'value': 'US'}
                ],
                    value='CA'
                )]),
    html.Br(),
    html.Div(["Please input the view numbers: ",
                html.Br(),
                dcc.Input(id='my-input-view-number', type='number', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Div(["Please input the likes: ",
                html.Br(),
                dcc.Input(id='my-input-like-number', type='number', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Div(["Please input the dislikes: ",
                html.Br(),
                dcc.Input(id='my-input-dislikes-number', type='number', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Div(["Please input the comment numbers: ",
                html.Br(),
                dcc.Input(id='my-input-comment-number', type='number', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Div(["Please select a category: ",
              dcc.Dropdown(
                 id='drp-category',
                 options=[
                    {'label': 'Entertainment', 'value': 9},
                    {'label': 'Music', 'value': 8},
                    {'label': 'Sports', 'value': 7},
                    {'label': 'Comedy', 'value': 6},
                    {'label': 'People & Blogs', 'value': 5},
                    {'label': 'Howto & Style', 'value': 4},
                    {'label': 'Film & Animation', 'value': 4},
                    {'label': 'Gaming', 'value': 3},
                    {'label': 'Science & Tech', 'value': 2},
                    {'label': 'News & Politics', 'value': 1},
                    {'label': 'Educatoin', 'value': 0},
                    {'label': 'Autos & Vehicles', 'value': 0},
                    {'label': 'Travel & Events', 'value': 0},
                    {'label': 'Pets & Animals', 'value': 0},
                ],
                    value=9
                )]),
    html.Br(),
    html.Button('Check', id='btn-check', n_clicks=0),
    html.Br(),
    html.Div(id='my-output-ai')
], style = {"width": "70%",})

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):    # Running as compiled
        return os.path.join(sys._MEIPASS, relative_path) # pylint: disable=no-member
    return os.path.join(os.path.abspath("."), relative_path)

@app.callback(
    dash.dependencies.Output('my-output-ai', 'children'),
    [dash.dependencies.Input('btn-check', 'n_clicks')],
    [dash.dependencies.Input('drp-country', 'value')],
    [dash.dependencies.Input('drp-category', 'value')],
    [dash.dependencies.State('my-input-view-number', 'value')],
    [dash.dependencies.State('my-input-like-number', 'value')],
    [dash.dependencies.State('my-input-dislikes-number', 'value')],
    [dash.dependencies.State('my-input-comment-number', 'value')]
)
def number_render(n_clicks, country, category, view_number, likes, dislikes, comments):

    if not (view_number is None or country is None or likes is None or dislikes is None or comments is None or category is None):
    #Based on the country to load the model of country
        
        model_file_name_view_number = f"model_view_number_{country}.joblib"
        model_file_name_view_number = resource_path(model_file_name_view_number)
        model_view_number = load(model_file_name_view_number)

        model_file_name_likes = f"model_likes_{country}.joblib"
        model_file_name_likes = resource_path(model_file_name_likes)
        model_likes = load(model_file_name_likes)

        model_file_name_dislikes = f"model_dislikes_{country}.joblib"
        model_file_name_dislikes = resource_path(model_file_name_dislikes)
        model_dislikes = load(model_file_name_dislikes)

        model_file_name_comments = f"model_comments_{country}.joblib"
        model_file_name_comments = resource_path(model_file_name_comments)
        model_comments = load(model_file_name_comments)

        model_file_name_category = f"model_category_{country}.joblib"
        model_file_name_category = resource_path(model_file_name_category)
        model_category = load(model_file_name_category)

        a1 = np.zeros((1,1))
        a1[0,0] = view_number
        prediction_view_number = model_view_number.predict(a1)
        a1[0,0] = likes
        prediction_likes = model_likes.predict(a1)
        a1[0,0] = dislikes
        prediction_dislikes = model_dislikes.predict(a1)
        a1[0,0] = comments
        prediction_comments = model_comments.predict(a1)
        a1[0,0] = category
        prediction_category = model_category.predict(a1)

        score_total = prediction_view_number[0] + prediction_likes[0] + prediction_dislikes[0] + prediction_comments[0] + prediction_category[0]
        
        return html.Div([
            html.Hr(),
            html.H2(children='AI predicts your scores of becoming the next trend video (Max: 100): {}'.format(score_total)),
            html.H3(children='Country: {}, View Numbers: {} Likes: {} DisLikes: {} Comments: {} Category: {} Score:{}'.format(country, view_number, likes, dislikes, comments, category, score_total), style = {'color': 'red'}),
            html.H3(children='View number score (Max: 24):{}'.format(prediction_view_number[0])),
            html.H3(children='Likes score (Max: 21):{}'.format(prediction_likes[0])),
            html.H3(children='Dislikes score (Max: 20):{}'.format(prediction_dislikes[0])),
            html.H3(children='Comments score (Max: 23):{}'.format(prediction_comments[0])),
            html.H3(children='Category score (Max: 12):{}'.format(prediction_category[0]))
        ])


if __name__ == '__main__':
    
    app.run_server(debug=False, port=9002)
