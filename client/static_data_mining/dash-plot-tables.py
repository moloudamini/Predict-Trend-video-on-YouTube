# reference to https://dash.plotly.com/layout
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
conn = mysql.connector.connect(user='user', password='password', host='host', database='database')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

sql = 'SELECT T3.title AS Video_category, T1.cnt_v AS Number_of_videos, T1.max_v AS Max_number_of_views, T1.min_v AS Min_number_of_views \
FROM (SELECT video_id, category_id, max(views) as max_v, min(views) as min_v, count(video_id) as cnt_v \
    FROM Videos_CA as v \
    INNER JOIN (SELECT video_id, views FROM Views_CA) AS r\
    USING(video_id) \
    group by category_id \
    order by max_v desc) as T1 \
INNER JOIN (SELECT category_id, snippet_id FROM Category) AS T2 \
ON T1.category_id = T2.category_id \
INNER JOIN (SELECT snippet_id, title FROM Snippet) AS T3 \
ON T2.snippet_id = T3.snippet_id' \

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_sql(sql, conn)
fig = px.bar(df, y="Video_category", x="Number_of_videos", color="Video_category", barmode="group", orientation='h')


sql2 = 'SELECT T1.Channel_title, T1.vid AS Number_of_videos, T1.max_v AS Max_number_of_views, T1.min_v AS Min_number_of_views \
FROM (SELECT v.video_id, video_title, channel_title, max(views) as max_v, min(views) as min_v, count(v.video_id) as vid \
      FROM Videos_CA as v \
      INNER JOIN (SELECT video_id, views FROM Views_CA) AS r \
      USING(video_id) \
      GROUP BY channel_title \
      ORDER BY max_v DESC LIMIT 20) AS T1' \
          
df2 = pd.read_sql(sql2, conn)
fig2 = px.bar(df2, y="Channel_title", x="Number_of_videos", color="Channel_title", barmode="group", orientation='h')


sql3 = 'SELECT T1.Video_title, T1.publish_date, T1.Publish_time, T1.Trending_date, T1.max_v AS Max_number_of_views, T1.min_v AS Min_number_of_views \
FROM (SELECT video_id, video_title, publish_date, publish_time, trending_date, max(views) as max_v, min(views) as min_v \
      FROM Videos_CA as v \
      INNER JOIN (SELECT video_id, trending_date, views FROM Views_CA) AS r \
      USING(video_id) \
      GROUP BY publish_time \
      ORDER BY max_v desc LIMIT 20) as T1' \

df3 = pd.read_sql(sql3, conn)
fig3 = px.bar(df3, y="Video_title", x="Max_number_of_views", color="Video_title", barmode="group", orientation='h')

sql4 = 'SELECT v.Publish_date, v.n_p AS Number_of_publish_videos, r.Trending_date, r.num_v AS Number_of_trend_videos, \
r.max_v AS Max_views, r.min_v AS Min_views, r.min_c as Min_comments, r.max_c as Max_comments \
FROM (SELECT video_id, publish_date, count(video_id) AS n_p \
FROM Videos_CA \
GROUP BY publish_date \
ORDER BY publish_date DESC) AS v \
INNER JOIN (SELECT video_id, trending_date, count(video_id) AS num_v , MAX(views) AS max_v, MIN(views) as min_v, MAX(comment_count) as max_c, \
MIN(comment_count) as min_c FROM Views_CA \
WHERE views >= (SELECT AVG(views) FROM Views_CA) \
GROUP BY trending_date) AS r \
USING (video_id) \
WHERE r.trending_date = v.publish_date and publish_date like \'2020%\' '

df4 = pd.read_sql(sql4, conn)

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=df4['Publish_date'],
    y=df4['Number_of_publish_videos'],
    name='Number_of_publish_videos',
    marker_color='blue'
    # orientation='h'
))
fig4.add_trace(go.Bar(
    x=df4['Publish_date'],
    y=df4['Number_of_trend_videos'],
    name='Number_of_trending_videos',
    marker_color='red'
    # orientation='h'
))


sql5 = 'SELECT T1.Video_title, T1.views AS Number_of_views, T1.Comment_count, T1.Publish_date, T1.Trending_date, T1.Publish_time, T1.Trending_time, \
IF (T1.ddiff >= 1, CONCAT(T1.ddiff , \' day(s)\'), CONCAT(SUBSTRING(T1.tdiff, 1, 2), \' :H \', SUBSTRING(T1.tdiff, 4, 2), \' :M \' , SUBSTRING(T1.tdiff, 7, 2), \' :S\')) AS time_for_trending \
FROM (SELECT video_id, video_title, publish_date, publish_time, trending_date, trending_time, TIME_FORMAT(TIMEDIFF(publish_time, trending_time), "%H %i %s") AS tdiff, \
    views, comment_count, DATEDIFF(trending_date , publish_date) AS ddiff \
	FROM Videos_CA \
    INNER JOIN (SELECT video_id, trending_date, trending_time, views, comment_count FROM Views_CA) AS r \
    USING (video_id) \
    GROUP BY video_title \
    ORDER BY views DESC LIMIT 10) AS T1' \

df5 = pd.read_sql(sql5, conn)

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    y=df5['Video_title'],
    x=df5['Number_of_views'],
    name='Number_of_views',
    marker_color='blue',
    orientation='h'
))
fig5.add_trace(go.Bar(
    y=df5['Video_title'],
    x=df5['Comment_count'],
    name='Number_of_comments',
    marker_color='red',
    orientation='h'
))

sql6 = 'SELECT T1.Video_title, T1.len AS Video_title_len, T1.Publish_date, T1.Publish_time, T1.Trending_date, T1.max_v AS Max_number_of_views, T1.min_v AS Min_number_of_views \
FROM (SELECT video_id, video_title, length(video_title) as len, publish_date, publish_time, trending_date, max(views) as max_v, min(views) as min_v \
      FROM Videos_CA as v \
      INNER JOIN (SELECT video_id, trending_date, views FROM Views_CA) AS r \
      USING(video_id) \
      group by publish_time \
      order by max_v desc limit 10) as T1 '

df6 = pd.read_sql(sql6, conn)
fig6 = px.bar(df6, y="Video_title", x="Video_title_len", color="Video_title", barmode="group", orientation='h')

sql7 = 'SELECT T1.Video_title, T1.Publish_date, T1.Trending_date, T1.Views, T1.Likes, T1.Dislikes \
FROM (SELECT s.video_id, video_title, channel_title, publish_date,trending_date, views, likes, dislikes \
      FROM Videos_CA as s \
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V \
	  USING(video_id) \
      group by video_title) AS T1 \
ORDER BY T1.views DESC LIMIT 10' 

df7 = pd.read_sql(sql7, conn)
fig7 = go.Figure()
fig7.add_trace(go.Bar(
    y=df7['Video_title'],
    x=df7['Views'],
    name='Number_of_views',
    marker_color='blue',
    orientation='h'
))
fig7.add_trace(go.Bar(
    y=df7['Video_title'],
    x=df7['Likes'],
    name='Number_of_likes',
    marker_color='red',
    orientation='h'
))
fig7.add_trace(go.Bar(
    y=df7['Video_title'],
    x=df7['Dislikes'],
    name='Number_of_dislikes',
    marker_color='yellow',
    orientation='h'
))

sql8 = 'SELECT T1.Video_title, T1.Publish_date, T1.Trending_date, T1.Views, T1.Likes, T1.Dislikes, \
ROUND (( LENGTH(T1.tags)- LENGTH( REPLACE (T1.tags, "#", "") )) / LENGTH("#") ) as Hashtag_frequency \
FROM (SELECT s.video_id, video_title, channel_title, tags, publish_date,trending_date, views, likes, dislikes \
      FROM Videos_CA as s \
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V \
	  USING(video_id) \
      group by video_title) AS T1 \
ORDER BY Hashtag_frequency DESC LIMIT 20'

df8 = pd.read_sql(sql8, conn)
fig8 = go.Figure()
# fig8.add_trace(go.Bar(
#     y=df8['Video_title'],
#     x=df8['Views'],
#     name='Number_of_views',
#     marker_color='green',
#     orientation='h'
# ))
# fig8.add_trace(go.Bar(
#     y=df8['Video_title'],
#     x=df8['Dislikes'],
#     name='Number_of_dislikes',
#     marker_color='red',
#     orientation='h'
# ))
fig8.add_trace(go.Bar(
    y=df8['Video_title'],
    x=df8['Hashtag_frequency'],
    name='Number_of_hashtags',
    marker_color='blue',
    orientation='h'
))


colors = {
    'background': 'white',
    'text': 'black'
    # 'background': '#111111',
    # 'text': '#7FDBFF'
}

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig4.update_layout(
    barmode='group',
    xaxis_tickangle=-45,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    xaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig5.update_layout(
    barmode='group',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1,
)

fig6.update_layout(
    barmode='group',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig7.update_layout(
    barmode='group',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)
fig8.update_layout(
    barmode='group',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    yaxis_tickfont_size=12,
    bargap=0.15, 
    bargroupgap=0.1 
)


app.layout = html.Div([
    html.H3(
        children='Relationship Between Trending Videos and Different Categories',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }    
    ), 
    dcc.Graph(
        id='example-graph-1',
        figure=fig
    ),
    html.H4(children='Relationship Between Between Trending Videos and Different Categories in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df), 
    html.H3(
        children='Relationship Between Trending Videos and Different Channels',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),   
    dcc.Graph(
        id='example-graph-2',
        figure=fig2
    ),
    html.H4(children='Relationship Between Trending Videos and Different Channels in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df2), 
    html.H3(
        children='Relationship Between Trending Videos and Different Video Titles',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),  
    dcc.Graph(
        id='example-graph-3',
        figure=fig3
    ),
    html.H4(children='Relationship Between Trending Videos and Different Video Titles in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df3),  
    html.H3(
        children='Relationship Between Number of Publish Videos and Number of Trending Videos',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),  
    dcc.Graph(
        id='example-graph-4', 
        figure=fig4
    ),
    html.H4(children='Relationship Between Number of Publish Videos and Trending Videos with Views and Comments in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df4),
    html.H3(
        children='Relationship Between Top 10 Trending Videos and Number of Views and Comments ',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),  
    dcc.Graph(
        id='example-graph-5', 
        figure=fig5
    ),
    html.H4(children='Relationship Between Top 10 Trending Videos and Their Trending Time in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df5),
    html.H3(
        children='Relationship Between Top 10 Trending Videos and Video Title Length',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ), 
    dcc.Graph(
        id='example-graph-6', 
        figure=fig6
    ), 
    html.H4(children='Relationship Between the Length of Video Titles and Trending Views in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df6),
    html.H3(
        children='Relationship Between Top 10 Trending Videos and Number of Likes and Dislikes',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ), 
    dcc.Graph(
        id='example-graph-7', 
        figure=fig7
    ), 
    html.H4(children='Relationship Between the Length of Video Titles and Number of Likes and Dislikes in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df7),
    html.H3(
        children='Relationship Between Trending Videos and Number of Hashtags, Likes and Dislikes',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ), 
    dcc.Graph(
        id='example-graph-8', 
        figure=fig8
    ), 
    html.H4(children='Relationship Between Trending Videos and Number of Hashtags, Likes and Dislikes in Canada',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df8)
])


if __name__ == '__main__':
    app.run_server(debug=True)
