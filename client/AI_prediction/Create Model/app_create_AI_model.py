#Reference: https://medium.com/ai%E8%82%A1%E4%BB%94/%E5%AD%B8%E6%9C%83%E7%94%A8%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92%E9%A0%90%E6%B8%AC%E8%82%A1%E5%83%B9-%E5%AE%8C%E6%95%B4%E6%B5%81%E7%A8%8B%E6%95%99%E5%AD%B8%E8%88%87%E5%AF%A6%E4%BD%9C-b057e7343ca4

import mysql.connector
import pandas as pd
import mysql.connector
import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from joblib import dump, load

conn = mysql.connector.connect(user='user', password='password', host='host', database='database')

def create_AI_model_for_likes(country=[]):

    sql = "SELECT A.likes as likes, \
            CASE WHEN A.likes <= 25000 THEN 0 \
            WHEN A.likes > 25000 AND A.likes <= 50000 then 4 \
            WHEN A.likes > 50000 AND A.likes <= 100000 then 11 \
            WHEN A.likes > 100000 AND A.likes <= 500000 then 17 \
            ELSE 21 END AS likes_score \
            FROM ( \
            SELECT video_id, IFNULL(likes, 0) AS likes \
            FROM db656_s6amini.Views_country) A" 

    for country_name in country:

        # Model 01: Handle AI model for views.
        sql = sql.replace("country", country_name)
        df = pd.read_sql(sql, conn)
        print(f"Read country:{country_name} success!")

        #remove null data to make the data more correct.
        df.dropna()

        # split percentage: 70%:30%
        split_point = int(len(df)*0.7)

        # produce training and test sample
        train = df.iloc[:split_point,:].copy()
        
        # training.
        train_X = train.drop('likes_score', axis = 1)
        train_y = train.likes_score

        # Create a decision tree.
        model = DecisionTreeClassifier(max_depth = 7)

        # Let AI learn.
        model.fit(train_X, train_y.astype('int'))

        #export model
        dump(model, f"model_likes_{country_name}.joblib")
        print(f"Create AI model_likes for country:{country_name} success!")

def create_AI_model_for_dislikes(country=[]):

    sql = "SELECT A.dislikes as dislikes, \
            CASE WHEN A.dislikes <= 10000 THEN 20 \
            WHEN A.dislikes > 10000 AND A.dislikes <= 32500 then 16 \
            WHEN A.dislikes > 32500 AND A.dislikes <= 75000 then 10 \
            WHEN A.dislikes > 75000 AND A.dislikes <= 100000 then 4 \
            ELSE 0 END AS dislikes_score \
            FROM ( \
            SELECT video_id, IFNULL(dislikes, 0) AS dislikes \
            FROM db656_s6amini.Views_country) A" 

    for country_name in country:

        # Model 01: Handle AI model for views.
        sql = sql.replace("country", country_name)
        df = pd.read_sql(sql, conn)
        print(f"Read country:{country_name} success!")

        #remove null data to make the data more correct.
        df.dropna()

        # split percentage: 70%:30%
        split_point = int(len(df)*0.7)

        # produce training and test sample
        train = df.iloc[:split_point,:].copy()
        
        # training.
        train_X = train.drop('dislikes_score', axis = 1)
        train_y = train.dislikes_score

        # Create a decision tree.
        model = DecisionTreeClassifier(max_depth = 7)

        # Let AI learn.
        model.fit(train_X, train_y.astype('int'))

        #export model
        dump(model, f"model_dislikes_{country_name}.joblib")
        print(f"Create AI model_dislikes for country:{country_name} success!")

def create_AI_model_for_category(country=[]):
 
    sql = "SELECT CASE WHEN title = 'Entertainment' THEN 9 \
            WHEN title = 'Music' THEN 8 \
            WHEN title = 'Sports' THEN 7 \
            WHEN title = 'Comedy' THEN 6 \
            WHEN title = 'People & Blogs' THEN 5 \
            WHEN title = 'Howto & Style' THEN 4 \
            WHEN title = 'Film & Animation' THEN 3 \
            WHEN title = 'Gaming' THEN 2 \
            WHEN title = 'Science & Tech' THEN 1 \
            ELSE 0 END AS title, \
            CASE WHEN title = 'Entertainment' THEN 4 \
            WHEN title = 'Music' THEN 2 \
            WHEN title = 'Sports' THEN 1 \
            WHEN title = 'Comedy' THEN 1 \
            WHEN title = 'People & Blogs' THEN 1 \
            WHEN title = 'Howto & Style' THEN 1 \
            WHEN title = 'Film & Animation' THEN 1 \
            WHEN title = 'Gaming' THEN 1 \
            WHEN title = 'Science & Tech' THEN 1 \
            ELSE 0 END AS title_score \
            FROM ( \
            SELECT  \
            A.video_id, \
            TRIM(IFNULL(D.title, '')) AS title  \
            FROM db656_s6amini.Views_country A \
            INNER JOIN db656_s6amini.Videos_country B ON A.video_id = B.video_id \
            INNER JOIN db656_s6amini.Category C ON B.category_id = C.category_id \
            INNER JOIN db656_s6amini.Snippet D ON C.snippet_id = D.snippet_id) A"

    for country_name in country:

        # Model 01: Handle AI model for views.
        sql = sql.replace("country", country_name)
        df = pd.read_sql(sql, conn)
        print(f"Read country:{country_name} success!")

        #remove null data to make the data more correct.
        df.dropna()

        # split percentage: 70%:30%
        split_point = int(len(df)*0.7)

        # produce training and test sample
        train = df.iloc[:split_point,:].copy()
        
        # training.
        train_X = train.drop('title_score', axis = 1)
        train_y = train.title_score

        # Create a decision tree.
        model = DecisionTreeClassifier(max_depth = 7)

        # Let AI learn.
        model.fit(train_X, train_y.astype('int'))

        #export model
        dump(model, f"model_category_{country_name}.joblib")
        print(f"Create AI model_categirt for country:{country_name} success!")


def create_AI_model_for_comments(country=[]):

    sql = "SELECT A.comment_count as comments, \
            CASE WHEN A.comment_count <= 1500 THEN 0 \
            WHEN A.comment_count > 1500 AND A.comment_count <= 3056 then 5 \
            WHEN A.comment_count > 3056 AND A.comment_count <= 7718 then 11 \
            WHEN A.comment_count > 7718 AND A.comment_count <= 14485 then 18 \
            ELSE 23 END AS comment_score  \
            FROM ( \
            SELECT video_id, IFNULL(comment_count, 0) AS comment_count \
            FROM db656_s6amini.Views_country) A" 

    for country_name in country:

        # Model 01: Handle AI model for views.
        sql = sql.replace("country", country_name)
        df = pd.read_sql(sql, conn)
        print(f"Read country:{country_name} success!")

        #remove null data to make the data more correct.
        df.dropna()

        # split percentage: 70%:30%
        split_point = int(len(df)*0.7)

        # produce training and test sample
        train = df.iloc[:split_point,:].copy()
        
        # training.
        train_X = train.drop('comment_score', axis = 1)
        train_y = train.comment_score

        # Create a decision tree.
        model = DecisionTreeClassifier(max_depth = 7)

        # Let AI learn.
        model.fit(train_X, train_y.astype('int'))

        #export model
        dump(model, f"model_comments_{country_name}.joblib")
        print(f"Create AI model_comments for country:{country_name} success!")
    

def create_AI_model_for_viewNumber(country=[]):

    
    sql = "SELECT views, \
            CASE WHEN A.views <= 53796 THEN 0 \
            WHEN A.views > 53796 AND A.views <= 777510 then 5 \
            WHEN A.views > 777510 AND A.views <= 1387466 then 12 \
            WHEN A.views > 1387466 AND A.views <= 2000000 then 19 \
            ELSE 24 END AS views_score \
            FROM ( \
            SELECT video_id, IFNULL(views, 0) AS views \
            FROM db656_s6amini.Views_country) A"

    for country_name in country:

        # Model 01: Handle AI model for views.
        sql = sql.replace("country", country_name)
        df = pd.read_sql(sql, conn)
        print(f"Read country:{country_name} success!")

        #remove null data to make the data more correct.
        df.dropna()

        # split percentage: 70%:30%
        split_point = int(len(df)*0.7)

        # produce training and test sample
        train = df.iloc[:split_point,:].copy()
        
        # training.
        train_X = train.drop('views_score', axis = 1)
        train_y = train.views_score

        # Create a decision tree.
        model = DecisionTreeClassifier(max_depth = 7)

        # Let AI learn.
        model.fit(train_X, train_y.astype('int'))

        #export model
        dump(model, f"model_view_number_{country_name}.joblib")
        print(f"Create AI model_view number for country:{country_name} success!")

    
if __name__ == '__main__':

    # Build country list.
    country = ['BR','CA','DE','FR','GB','IN','JP','KR','MX','RU','US']
    
    # Call the function to build AI models.
    create_AI_model_for_viewNumber(country)
    create_AI_model_for_comments(country)
    create_AI_model_for_likes(country)
    create_AI_model_for_dislikes(country)
    create_AI_model_for_category(country)
    conn.close()
    
