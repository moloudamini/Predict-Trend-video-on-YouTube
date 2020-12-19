USE database_name;

-- The top 3 videos that their views are higher than the average of views based on a specific publish_time and trending_date
SELECT DISTINCT T1.*, T3.title
FROM (SELECT video_title, channel_title, publish_date, publish_time, V.trending_date, V.views, V.likes, V.dislikes, V.comment_count, category_id
      FROM Videos_CA 
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA
      WHERE views >=(SELECT AVG(views) FROM Views_CA)) AS V
	  USING(video_id)
      where publish_date like "2020-08-21%" and publish_time like "%" and
      trending_date between "2020-08-22" and "2020-08-28"
      GROUP BY video_title) AS T1 
INNER JOIN (SELECT category_id, snippet_id FROM Category) AS T2 
ON T1.category_id = T2.category_id
INNER JOIN (SELECT snippet_id, title FROM Snippet) AS T3
ON T2.snippet_id = T3.snippet_id
ORDER BY T1.views DESC LIMIT 3;

-- The top 3 videos with highest number of views based on a specific publish_time and trending_date
SELECT T1.*, T3.title
FROM (SELECT s.video_id, video_title, channel_title, publish_date, publish_time, trending_date, views, likes, dislikes, comment_count, category_id
      FROM Videos_CA as s
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V
	  USING(video_id)
      where publish_date like "2020-08-21%" and publish_time like "%" and 
      trending_date between "2020-08-22" and "2020-08-28"
      group by video_title) AS T1 
INNER JOIN (SELECT category_id, snippet_id FROM Category) AS T2 
ON T1.category_id = T2.category_id
INNER JOIN (SELECT snippet_id, title FROM Snippet) AS T3
ON T2.snippet_id = T3.snippet_id
ORDER BY T1.views DESC LIMIT 3;

-- the relationship between each channel and the number of its videos with differnt title based on max and min number of views
SELECT T1.channel_title, T1.video_title, T1.vid AS number_of_videos, T1.max_v AS max_number_of_views, T1.min_v AS min_number_of_views
FROM (SELECT video_id, video_title, channel_title, max(views) as max_v, min(views) as min_v, count(v.video_id) as vid
      FROM Videos_CA as v
      INNER JOIN (SELECT video_id, views FROM Views_CA) AS r
      USING(video_id)
      group by video_title, channel_title
      order by max_v desc) as T1;  
      
-- the relationship between each channel and the total number of its trending videos with max and min number of views
SELECT T1.channel_title, T1.vid AS number_of_videos, T1.max_v AS max_number_of_views, T1.min_v AS min_number_of_views
FROM (SELECT video_id, video_title, channel_title, max(views) as max_v, min(views) as min_v, count(v.video_id) as vid
      FROM Videos_CA as v
      INNER JOIN (SELECT video_id, views FROM Views_CA) AS r
      USING(video_id)
      GROUP BY channel_title
      ORDER BY max_v DESC) AS T1; 
      
-- the relationship between the trending videos and their title       
SELECT T1.video_title, T1.publish_date, T1.publish_time, T1.trending_date, T1.max_v AS max_number_of_views, T1.min_v AS min_number_of_views
FROM (SELECT video_id, video_title, publish_date, publish_time, trending_date, max(views) as max_v, min(views) as min_v
      FROM Videos_CA as v
      INNER JOIN (SELECT video_id, trending_date, views FROM Views_CA) AS r
      USING(video_id)
      GROUP BY publish_time
      ORDER BY max_v desc LIMIT 20) as T1;  
 
 -- the relationship between the trending videos and the length of their titles       
SELECT T1.video_title, T1.len AS video_title_len , T1.publish_date, T1.publish_time, T1.trending_date, T1.max_v AS max_number_of_views, T1.min_v AS min_number_of_views
FROM (SELECT video_id, video_title, length(video_title) as len, publish_date, publish_time, trending_date, max(views) as max_v, min(views) as min_v
      FROM Videos_CA as v
      INNER JOIN (SELECT video_id, trending_date, views FROM Views_CA) AS r
      USING(video_id)
      group by publish_time
      order by max_v desc LIMIT 10) as T1; 
      
-- the relationship between the trending videos and differnt categories     
SELECT  T3.title AS video_category, T1.cnt_v AS number_of_videos, T1.max_v AS max_number_of_views, T1.min_v AS min_number_of_views
FROM (SELECT video_id, category_id, max(views) as max_v, min(views) as min_v, count(video_id) as cnt_v
      FROM Videos_CA as v
      INNER JOIN (SELECT video_id, views FROM Views_CA) AS r
      USING(video_id)
      group by category_id
      order by max_v desc) as T1
INNER JOIN (SELECT category_id, snippet_id FROM Category) AS T2 
ON T1.category_id = T2.category_id
INNER JOIN (SELECT snippet_id, title FROM Snippet) AS T3
ON T2.snippet_id = T3.snippet_id; 

-- the relationship between the number of publish videos in each date and the number of trend videos in a given date 
-- how many of published videos have been popular?       
SELECT v.publish_date, v.n_p AS number_of_publish_videos, r.trending_date, r.num_v AS number_of_trend_videos, r.max_v AS max_number_of_views, r.min_v AS min_number_of_views
FROM (SELECT video_id, publish_date, count(video_id) AS n_p
FROM Videos_CA 
GROUP BY publish_date
ORDER BY publish_date DESC) AS v
INNER JOIN (SELECT video_id, trending_date, count(video_id) AS num_v , MAX(views) AS max_v, MIN(views) as min_v FROM Views_CA 
WHERE views >= (SELECT AVG(views) FROM Views_CA)
GROUP BY trending_date) AS r
USING (video_id)
WHERE r.trending_date = v.publish_date;

-- the relationship between the trending videos and the number of comments
SELECT v.publish_date, v.n_p AS number_of_publish_videos, r.trending_date, r.n_v AS number_of_trend_videos, r.m as max_number_of_comments, r.mi as min_number_of_comments
FROM (SELECT video_id, publish_date, count(video_id) AS n_p
FROM Videos_CA 
GROUP BY publish_date
ORDER BY publish_date DESC) AS v
INNER JOIN (SELECT video_id, trending_date, max(comment_count) as m, min(comment_count) as mi, count(video_id) AS n_v FROM Views_CA 
WHERE views >= (SELECT AVG(views) FROM Views_CA)
GROUP BY trending_date) AS r
USING (video_id)
WHERE r.trending_date = v.publish_date;
      
-- the relationship between the trending videos and the number of likes
SELECT v.publish_date, v.n_p AS number_of_publish_videos, r.trending_date, r.n_v AS number_of_trend_videos, r.m as max_number_of_likes, r.mi as min_number_of_likes
FROM (SELECT video_id, publish_date, count(video_id) AS n_p
FROM Videos_CA 
GROUP BY publish_date
ORDER BY publish_date DESC) AS v
INNER JOIN (SELECT video_id, trending_date, max(likes) as m, min(likes) as mi, count(video_id) AS n_v FROM Views_CA 
WHERE views >= (SELECT AVG(views) FROM Views_CA)
GROUP BY trending_date) AS r
USING (video_id)
WHERE r.trending_date = v.publish_date;

-- the relationship between the trending videos and the number of dislikes
SELECT v.publish_date, v.n_p AS number_of_publish_videos, r.trending_date, r.n_v AS number_of_trend_videos, r.m as max_number_of_dislikes, r.mi as min_number_of_dislikes
FROM (SELECT video_id, publish_date, count(video_id) AS n_p
FROM Videos_CA 
GROUP BY publish_date
ORDER BY publish_date DESC) AS v
INNER JOIN (SELECT video_id, trending_date, max(dislikes) as m, min(dislikes) as mi, count(video_id) AS n_v FROM Views_CA 
WHERE views >= (SELECT AVG(views) FROM Views_CA)
GROUP BY trending_date) AS r
USING (video_id)
WHERE r.trending_date = v.publish_date;

-- relationship between top 10 trending videos and their trending time (how long did it take to become papular?)
SELECT T1.video_title, T1.views AS number_of_views, T1.comment_count, T1.publish_date, T1.trending_date, T1.publish_time, T1.trending_time,
IF (T1.ddiff >= 1, CONCAT(T1.ddiff , ' day(s)'), CONCAT(SUBSTRING(T1.tdiff, 1, 2), ' :H ', SUBSTRING(T1.tdiff, 4, 2), ' :M ' , SUBSTRING(T1.tdiff, 7, 2), ' :S')) AS time_for_trending
FROM (SELECT video_id, video_title, publish_date, publish_time, trending_date, trending_time, TIME_FORMAT(TIMEDIFF(publish_time, trending_time), "%H %i %s") AS tdiff, 
      views, comment_count, DATEDIFF(trending_date , publish_date) AS ddiff
	  FROM Videos_CA
      INNER JOIN (SELECT video_id, trending_date, trending_time, views, comment_count FROM Views_CA) AS r
      USING (video_id)
      GROUP BY video_title
      ORDER BY views DESC LIMIT 10) AS T1;
      
-- the frequecny of a spesific word in the title of trending videos
SELECT video_title, ROUND (( LENGTH(video_title)- LENGTH( REPLACE (video_title, "video", "") )) / LENGTH("video") ) AS frequency
FROM Videos_CA
ORDER BY frequency DESC;

-- relationship between the top 10 trending videos and the number of views, likes and dislikes
SELECT T1.video_title, T1.publish_date, T1.trending_date, T1.views, T1.likes, T1.dislikes
FROM (SELECT s.video_id, video_title, channel_title, publish_date,trending_date, views, likes, dislikes
      FROM Videos_CA as s
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V
	  USING(video_id)
      group by video_title) AS T1 
ORDER BY T1.views DESC LIMIT 10;


-- is there hashtag in top 10 trending videos in canada?
SELECT T1.video_title, T1.publish_date, T1.trending_date, T1.views, T1.likes, T1.dislikes, ROUND (( LENGTH(T1.tags)- LENGTH( REPLACE (T1.tags, "#", "") )) / LENGTH("#") ) as Hashtag_frequency
FROM (SELECT s.video_id, video_title, channel_title, tags, publish_date,trending_date, views, likes, dislikes
      FROM Videos_CA as s
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V
	  USING(video_id)
      group by video_title) AS T1 
ORDER BY T1.views DESC LIMIT 10;

-- relationship between the trending videos and the number of hashtags in their tags
SELECT T1.video_title, T1.publish_date, T1.trending_date, T1.views, T1.likes, T1.dislikes, ROUND (( LENGTH(T1.tags)- LENGTH( REPLACE (T1.tags, "#", "") )) / LENGTH("#") ) as Hashtag_frequency
FROM (SELECT s.video_id, video_title, channel_title, tags, publish_date,trending_date, views, likes, dislikes
      FROM Videos_CA as s
      INNER JOIN (SELECT video_id, trending_date, views, likes, dislikes, comment_count FROM Views_CA) AS V
	  USING(video_id)
      group by video_title) AS T1 
ORDER BY Hashtag_frequency DESC;
