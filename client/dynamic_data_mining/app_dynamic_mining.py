#Reference: https://dash.plotly.com/basic-callbacks
import sys
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

from datetime import date
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import mysql.connector
conn = mysql.connector.connect(user='user', password='password', host='host', database='database')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_graph(df, graph_type):

    if graph_type == 1:
        fig = px.scatter(df, x="likes", y="dislikes",
                    size="views", color="location_id", hover_name="video_title",
                    log_x=True, size_max=60)
        return html.Div([
            dcc.Graph(
                id='top10videosbyViews-graph',
                figure=fig)
            ])
    else:
        fig1 = px.scatter(df, x="likes", y="dislikes",
                size="comment_count", color="location_id", hover_name="video_title",
                log_x=True, size_max=60)
        return html.Div([
            dcc.Graph(
                id='top10videosbyComments-graph',
                figure=fig1)
    ])

def generate_table(df, max_rows=20):
   
    rows = df.shape[0]
    i = 0
    rank = []
    if rows > 0:
        while i < rows:
            i = i + 1 
            rank.append(i)
    
    df.insert(0, "rank", rank, False)

    return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df.columns])] +

            # Body
            [html.Tr([
                html.Td(df.iloc[i][col]) if col != 'link' else html.Td(html.A(href=df.iloc[i]['link'], children=df.iloc[i][col], target='_blank')) for col in df.columns 
        ]) for i in range(len(df))]
    )


#app.layout = html.Div(children=[
app.layout = html.Div(children=[
    html.H1(children='Dynamic Data Mining', style={'textAlign': 'center'}),
    html.Hr(),
    html.Div(["Please select a date: ",
            html.Br(),
            dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=date(2017, 1, 1),
            max_date_allowed=date(2020, 12, 31),
            initial_visible_month=date(2020, 11, 10),
            date=date(2020, 11, 10))]),
    html.Br(),
    html.Div(["Please select a category: ",
              dcc.Dropdown(
                 id='drp-category',
                 options=[
                    {'label': 'Entertainment', 'value': 'Entertainment'},
                    {'label': 'Music', 'value': 'Music'},
                    {'label': 'Sports', 'value': 'Sports'},
                    {'label': 'Comedy', 'value': 'Comedy'},
                    {'label': 'People & Blogs', 'value': 'People & Blogs'},
                    {'label': 'Howto & Style', 'value': 'Howto & Style'},
                    {'label': 'Film & Animation', 'value': 'Film & Animation'},
                    {'label': 'Gaming', 'value': 'Gaming'},
                    {'label': 'Science & Tech', 'value': 'Science & Tech'},
                    {'label': 'News & Politics', 'value': 'News & Politics'},
                    {'label': 'Educatoin', 'value': 'Educatoin'},
                    {'label': 'Autos & Vehicles', 'value': 'Autos & Vehicles'},
                    {'label': 'Travel & Events', 'value': 'Travel & Events'},
                    {'label': 'Pets & Animals', 'value': 'Pets & Animals'},
                ],
                    value='Entertainment'
                )]),
    html.Br(),
    html.Div(["Please input video title: ",
                html.Br(),
                dcc.Input(id='my-input-video-title', type='text', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Div(["Please input the name of hash tag: ",
                html.Br(),
                dcc.Input(id='my-input-hash-tag', type='text', style={
                'width': '100%'
            })]),
    html.Br(),
    html.Button('Query', id='btn-query', n_clicks=0),
    html.Br(),
    html.Div(id='my-output-dynamic-mining'),
    html.Hr()
], style = {"width": "70%",})


@app.callback(
    dash.dependencies.Output('my-output-dynamic-mining', 'children'),
    [dash.dependencies.Input('btn-query', 'n_clicks')],
    [dash.dependencies.Input('my-date-picker-single', 'date')],
    [dash.dependencies.Input('drp-category', 'value')],
    [dash.dependencies.State('my-input-video-title', 'value')],
    [dash.dependencies.State('my-input-hash-tag', 'value')],
)
def number_render(n_clicks, date_value, video_category, video_name, hash_tag_name):

    #build sql
    sql = '''SELECT T.video_id, T.video_title, CONCAT('https://www.youtube.com/watch?v=', SUBSTRING_INDEX(SUBSTRING_INDEX(T.video_id, '_', 2), '_', -1)) AS link, 
            T.views, T.likes, T.dislikes, T.comment_count, T.location_id, T.title as Category, T.publish_date, T.tags 
            FROM ( 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_CA A 
            INNER JOIN db656_s6amini.Videos_CA B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_BR A 
            INNER JOIN db656_s6amini.Videos_BR B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_DE A 
            INNER JOIN db656_s6amini.Videos_DE B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_FR A 
            INNER JOIN db656_s6amini.Videos_FR B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_GB A 
            INNER JOIN db656_s6amini.Videos_GB B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_IN A 
            INNER JOIN db656_s6amini.Videos_IN B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_KR A 
            INNER JOIN db656_s6amini.Videos_KR B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_MX A 
            INNER JOIN db656_s6amini.Videos_MX B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_RU A 
            INNER JOIN db656_s6amini.Videos_RU B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE 
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10)
            UNION  
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_JP A 
            INNER JOIN db656_s6amini.Videos_JP B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10) 
            UNION 
            (SELECT A.video_id, A.views, A.likes, A.dislikes, A.comment_count, A.location_id, B.video_title, D.title, B.publish_date, B.tags 
            FROM db656_s6amini.Views_US A 
            INNER JOIN db656_s6amini.Videos_US B ON A.video_id = B.video_id 
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id 
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id 
            WHERE A.trending_date = QUERYDATE 
            AND D.title = QUERYCATEGORY AND B.tags like QUERYTAG AND B.video_title like QUERYTITLE
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC LIMIT 10)) T
            ORDER BY views DESC, comment_count DESC, likes DESC, dislikes ASC '''

    #Replace date in sql.
    date_object = date.fromisoformat(date_value)
    date_select_string = date_object.strftime('%Y-%m-%d')
    sql = sql.replace("QUERYDATE", f"'{date_select_string}'")

    #Replace category in sql.
    sql = sql.replace("QUERYCATEGORY", f"'{video_category}'")           

    #Process qeurying hash tag name
    if video_name is not None:
        sql = sql.replace("QUERYTITLE", f"'%{video_name}%'")
    else:
        sql = sql.replace("AND B.video_title like QUERYTITLE", "")

    if hash_tag_name is not None:
        sql = sql.replace("QUERYTAG", f"'%{hash_tag_name}%'")
    else:
        sql = sql.replace("AND B.tags like QUERYTAG", "")

    df = pd.read_sql(sql, conn, index_col = 'video_id')

    if df.shape[0] > 0:
        return html.Div([
            html.Hr(),
            html.H3(children='Input data - Selected date: {} Searching category: {} Searching video title: {} Searching hash tag: {}'.format(date_select_string, video_category, video_name, hash_tag_name), style = {'color': 'red'}),
            html.Hr(),
            html.H3('Top 10 views in all locations'),
            generate_graph(df, 1),
            html.H3('Top 10 comments in all locations'),
            generate_graph(df, 0),
            html.H3('Deatils of top 110 trends videos in all countries'),
            generate_table(df)
        ])
    else:
        return html.Div([
            html.Hr(),
            html.H3(children='Input data - *Selected date: {} *Searching category: {} *Searching video title: {} *Searching hash tag: {}'.format(date_select_string, video_category, video_name, hash_tag_name), style = {'color': 'red'}),
            html.Hr(),
            html.H3('Top 10 views in all locations'),
            html.H3(f'No data for date:{date_select_string}', style = {'color': 'blue'}),
            html.H3('Top 10 comments in all locations'),
            html.H3(f'No data for date:{date_select_string}', style = {'color': 'blue'}),
            html.H3('Deatils of top 110 trends videos in all countries'),
            html.H3(f'No data for date:{date_select_string}', style = {'color': 'blue'})
        ])


if __name__ == '__main__':
    app.run_server(debug=False, port=9001)

    
