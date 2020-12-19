import csv
import mysql.connector

connection = mysql.connector.connect(user='user', password='password', host='host', database='database',port='port')
cursor = connection.cursor()
cursor.execute('SET NAMES utf8mb4;')
cursor.execute('SET CHARACTER SET utf8mb4;')
cursor.execute('SET character_set_connection=utf8mb4;')

with open('CAviews.csv', 'r', encoding="UTF-8") as file:
    csv_file = csv.reader(file, delimiter=',')
    Line_Check = True

    for row in csv_file:
        if Line_Check:
            Line_Check = False
            continue
        INSERT_CMD = ("INSERT INTO Views_CAa"
        "(video_id, trending_date, views, likes, dislikes, comment_count)"
        " VALUES(%s, %s, %s, %s, %s, %s)")
        cursor.execute(INSERT_CMD, row)
connection.commit()
print("Data has been inserted into the TABLE")

# with open('CAvideos.csv', 'r', encoding="UTF-8") as file:
#     csv_file = csv.reader(file, delimiter=',')
#     Line_Check = True

#     for row in csv_file:
#         if Line_Check:
#             Line_Check = False
#             continue
#         INSERT_CMD = ("INSERT INTO Videos_CA"
#                        "(video_id, video_title, channel_title, category_id, publish_time, tags, thumbnail_link, comments_disabled, ratings_disabled, video_error_or_removed, description)"
#                        " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
#         cursor.execute(INSERT_CMD, row)
# connection.commit()
# print("Data has been inserted into the TABLE")

