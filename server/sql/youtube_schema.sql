CREATE DATABASE IF NOT EXISTS database_name;
USE database_name;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Videos_CA;
CREATE TABLE IF NOT EXISTS Videos_CA(
`video_id` varchar(20) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_CA;
CREATE TABLE IF NOT EXISTS Views_CA(
`video_id` varchar(20) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_CA;
CREATE TABLE IF NOT EXISTS Channel_CA(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_DE;
CREATE TABLE IF NOT EXISTS Videos_DE(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_DE;
CREATE TABLE IF NOT EXISTS Views_DE(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_DE;
CREATE TABLE IF NOT EXISTS Channel_DE(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_FR;
CREATE TABLE IF NOT EXISTS Videos_FR(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_FR;
CREATE TABLE IF NOT EXISTS Views_FR(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_FR;
CREATE TABLE IF NOT EXISTS Channel_FR(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_GB;
CREATE TABLE IF NOT EXISTS Videos_GB(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_GB;
CREATE TABLE IF NOT EXISTS Views_GB(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_GB;
CREATE TABLE IF NOT EXISTS Channel_GB(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_IN;
CREATE TABLE IF NOT EXISTS Videos_IN(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_IN;
CREATE TABLE IF NOT EXISTS Views_IN(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_IN;
CREATE TABLE IF NOT EXISTS Channel_IN(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_JP;
CREATE TABLE IF NOT EXISTS Videos_JP(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_JP;
CREATE TABLE IF NOT EXISTS Views_JP(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_JP;
CREATE TABLE IF NOT EXISTS Channel_JP(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_KR;
CREATE TABLE IF NOT EXISTS Videos_KR(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_KR;
CREATE TABLE IF NOT EXISTS Views_KR(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_KR;
CREATE TABLE IF NOT EXISTS Channel_KR(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_MX;
CREATE TABLE IF NOT EXISTS Videos_MX(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_MX;
CREATE TABLE IF NOT EXISTS Views_MX(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_MX;
CREATE TABLE IF NOT EXISTS Channel_MX(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  

DROP TABLE IF EXISTS Videos_RU;
CREATE TABLE IF NOT EXISTS Videos_RU(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_RU;
CREATE TABLE IF NOT EXISTS Views_RU(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_RU;
CREATE TABLE IF NOT EXISTS Channel_RU(
`channel_id` int NOT NULL AUTO_INCREMENT,
`channel_title` varchar(100) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_US;
CREATE TABLE IF NOT EXISTS Videos_US(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_US;
CREATE TABLE IF NOT EXISTS Views_US(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_US;
CREATE TABLE IF NOT EXISTS Channel_US(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Videos_BR;
CREATE TABLE IF NOT EXISTS Videos_BR(
`video_id` varchar(11) DEFAULT NULL,
`video_title` varchar(500) DEFAULT NULL,
`channel_title` varchar(200) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`category_id` int(11) DEFAULT NULL,
`channel_id` int(11) DEFAULT NULL,
`publish_time` varchar(20) DEFAULT NULL,
`publish_date` varchar(20) DEFAULT NULL,
`tags` mediumtext DEFAULT NULL,
`thumbnail_link` varchar(255) DEFAULT NULL,
`comments_disabled` char(5) DEFAULT NULL,
`ratings_disabled` char(5) DEFAULT NULL,
`video_error_or_removed` char(5) DEFAULT NULL,
`description` mediumtext DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Views_BR;
CREATE TABLE IF NOT EXISTS Views_BR(
`video_id` varchar(11) DEFAULT NULL,
`trending_date` varchar(20) DEFAULT NULL,
`trending_time` varchar(20) DEFAULT NULL,
`views` int DEFAULT NULL,
`likes` int DEFAULT NULL,
`dislikes` int DEFAULT NULL,
`comment_count` int DEFAULT NULL,
`location_id` char(2) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Channel_BR;
CREATE TABLE IF NOT EXISTS Channel_BR(
`channel_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_title` varchar(200) DEFAULT NULL,
`location_id` char(2) DEFAULT NULL,
PRIMARY KEY (`channel_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS Location;
CREATE TABLE IF NOT EXISTS Location(
`location_id` char(2) DEFAULT NULL,
`country` varchar(20) DEFAULT NULL,
`data_import_date` varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Category;
CREATE TABLE IF NOT EXISTS Category(
`category_id` int(11) DEFAULT NULL,
`video_kind` varchar(255) DEFAULT NULL,
`etag1` varchar(255) DEFAULT NULL,
`etag2` varchar(255) DEFAULT NULL,
`snippet_id` int(11) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DROP TABLE IF EXISTS Snippet;
CREATE TABLE IF NOT EXISTS Snippet(
`snippet_id` int(11) NOT NULL AUTO_INCREMENT,
`channel_id` varchar(255) DEFAULT NULL,
`title` varchar(100) DEFAULT NULL,
`assignable` char(5) DEFAULT NULL,
 PRIMARY KEY (`snippet_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

SET FOREIGN_KEY_CHECKS = 1;

