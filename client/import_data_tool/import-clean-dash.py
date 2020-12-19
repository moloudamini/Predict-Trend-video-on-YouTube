import os
import dash
import base64
import csv
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash_html_components.Div import Div
from flask import Flask, send_from_directory
from urllib.parse import quote as urlquote
import mysql.connector

conn = mysql.connector.connect(user='s6amini', password='saraamini', host='marmoset04.shoshin.uwaterloo.ca', database='db656_s6amini')
cursor = conn.cursor()
cursor.execute('SET NAMES utf8mb4;')
cursor.execute('SET CHARACTER SET utf8mb4;')
cursor.execute('SET character_set_connection=utf8mb4;')

UPLOAD_DIRECTORY = "/project/upload_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

colors = {
    'background': 'white',
    'text': 'black'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children= [
        html.H1(
            children="Import Latest Youtube Date Files to Our Database",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.A("Please visit this website to download the latest CA_youtube_trending_data.csv file: ", href='https://www.kaggle.com/rsrishav/youtube-trending-video-dataset/?select=CA_youtube_trending_data.csv'),
        html.H3(
            children="Please upload CA_youtube_trending_data.csv file in this page: ",
            style={
                'textAlign': 'left',
                'color': colors['text']
            }
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "max-width": "600px",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin-left": "10px",
                "margin-right": "50px"
            },
            multiple=True,
        ),
        html.H2("Available Files List:"),
        html.Ul(id="file-list"),
        html.H3("You can choose one of these buttons to load and clean the latest youtube data to our database:"),
        html.Div(style = {"margin-right": "10px", "margin-left": "50px",}, children = [
            html.H3("First, you have to insert data into temporary table: "),
            html.Button("Import data to temporary table", id="tbtn", n_clicks=0),
        ]),

        html.Div(style = {"margin-right": "10px", "margin-left": "50px",}, children = [
            html.H3("Second, you can insert data into video table or view table: "),
            html.Button("Import data to video table", id="vbtn", n_clicks=0),
            html.Button("Import data to view table", id="wbtn", n_clicks=0),
        ]),
        
        html.Div(style = {"margin-right": "10px", "margin-left": "50px",}, children = [
            html.H3("Finally, it needs to clean data for video table or view table to be compatible with previous data: "),
            html.Button("clean data in video table", id="clnbtn1", n_clicks=0),
            html.Button("clean data in view table", id="clnbtn2", n_clicks=0),
        ]),
        html.Div(id='import-clean')
        
])


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]
    

def insert_into_data_table():
    files = uploaded_files()
    for filename in files:
        with open(os.path.join(UPLOAD_DIRECTORY, filename), 'r', encoding="UTF-8") as file:
            csv_file = csv.reader(file, delimiter=',')
            Line_Check = True

            for row in csv_file:
                if Line_Check:
                    Line_Check = False
                    continue
                INSERT_CMD = ("INSERT INTO Tmp_data_table"
                            "(video_id, video_title, publish_time, channel_id, channel_title, category_id, trending_time, tags, views, likes,	dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description)"
                            " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(INSERT_CMD, row)
        conn.commit()


def insert_into_videos_table():
    sql = 'INSERT INTO Tmp_videos_table (video_id, video_title, publish_time, channel_title, category_id, tags, thumbnail_link, comments_disabled, ratings_disabled, description) \
           SELECT concat( id ,"_", video_id) as video_id, video_title,publish_time, channel_title, category_id, tags, thumbnail_link, comments_disabled, ratings_disabled, description \
           FROM Tmp_data_table'
    cursor.execute(sql)
    conn.commit()
    

def insert_into_views_table():
    sql = 'INSERT INTO Tmp_views_table (video_id, trending_time, views, likes,	dislikes, comment_count) \
           SELECT concat( id ,"_", video_id) as video_id, trending_time, views, likes, dislikes, comment_count \
           FROM Tmp_data_table'   
    cursor.execute(sql)
    conn.commit()
    
def clean_videos_table ():
    sql = 'UPDATE Tmp_videos_table SET \
            video_error_or_removed = \'FALSE\', \
            location_id= \'CA\', \
            publish_date = SUBSTRING_INDEX(publish_time, \'T\', 1), \
			publish_time = SUBSTRING_INDEX(SUBSTRING_INDEX(publish_time, \'T\', 2), \'T\', -1) \
            WHERE video_error_or_removed is NULL and location_id is NULL' 

    cursor.execute(sql)  
    conn.commit()
    

def clean_views_table ():
    sql = 'UPDATE Tmp_views_table SET \
            location_id= \'CA\', \
            trending_date = SUBSTRING_INDEX(trending_time, \'T\', 1), \
			trending_time = SUBSTRING_INDEX(SUBSTRING_INDEX(trending_time, \'T\', 2), \'T\', -1) \
            WHERE location_id is NULL' 

    cursor.execute(sql)  
    conn.commit()


@app.callback(Output('import-clean', 'children'),
              Input('tbtn', 'n_clicks'),
              Input('vbtn', 'n_clicks'),
              Input('wbtn', 'n_clicks'),
              Input('clnbtn1', 'n_clicks'),
              Input('clnbtn2', 'n_clicks'))
def displayClick(tbtn, vbtn, wbtn,clnbtn1,clnbtn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'tbtn' in changed_id:
        insert_into_data_table()
        msg ='Input file has been inserted into temporary table'
    elif 'vbtn' in changed_id:
        insert_into_videos_table()
        msg ='Input file has been inserted into video table'
    elif 'wbtn' in changed_id:
        insert_into_views_table()
        msg ='Input file has been inserted into view table'
    elif 'clnbtn1' in changed_id:
        clean_videos_table ()
        msg = 'video table has been cleaned'     
    elif 'clnbtn2' in changed_id:
        clean_views_table ()
        msg = 'view table has been cleaned'    
    else:
        msg = 'None of the buttons have been selected yet'
    return html.Div(msg)


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

