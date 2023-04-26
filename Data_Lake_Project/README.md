# Project 4 Udacity DEND: Data Lake

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, I have been tasked with building an ETL pipeline that extracts their data from S3, process them using Spark, and load the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

In this project, I have applied what I learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3.

## DataSets

The Two datasets we are using for this project are Song data set and the log data set.

Example of the data in the dataset.
Song Data
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

Log Data
```
{"artist": null, "auth": "Logged In", "firstName": "Walter", "gender": "M", "itemInSession": 0, "lastName": "Frye", "length": null, "level": "free", "location": "San Francisco-Oakland-Hayward, CA", "method": "GET","page": "Home", "registration": 1540919166796.0, "sessionId": 38, "song": null, "status": 200, "ts": 1541105830796, "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"", "userId": "39"}

```

## Schema for Song Play Analysis

### Fact Table

songplays - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

users - users in the app
user_id, first_name, last_name, gender, level
songs - songs in music database
song_id, title, artist_id, year, duration
artists - artists in music database
artist_id, name, location, lattitude, longitude
time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

## Project Files

The project folder includes two files and two folders:

- etl.py is where the dats is loaded from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
- dl.cfg is where the aws keys are for S3 access
- data folder contains local data files
- output folder contains the local run output files

## Running this Project

Fill out dl.cfg file with the Key, Secret details for S3 creation
On terminal run

```
Python etl.py
```

### Author

Anju Mercian and the Udacity Team.