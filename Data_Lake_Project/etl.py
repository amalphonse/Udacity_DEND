import configparser
from datetime import datetime
import os
from pyspark.sql.types import TimestampType
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format, dayofweek


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Loads data from the song data dataset, extracts columns to
    create song and artists table and write the data as a
    parquet file to load into S3.

    Parameters
    spark: the spark session
    input_data: the folder where the song_data resides
    output_data: the folder where the parquet file are going to be stored.
    """
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/*/*/*/*.json")

    # read song data file
    df = spark.read.json(song_data)

    df.createOrReplaceTempView("song_data_table")

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title',
                            'artist_id', 'year', 'duration') \
        .dropDuplicates()

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id") \
               .mode('overwrite').parquet(os.path.join(output_data, 'songs'))

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location',
                              'artist_latitude', 'artist_longitude') \
        .withColumnRenamed('artist_name', 'name') \
        .withColumnRenamed('artist_location', 'location') \
        .withColumnRenamed('artist_latitude', 'latitude') \
        .withColumnRenamed('artist_longitude', 'longitude') \
        .dropDuplicates()

    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(
        os.path.join(output_data, 'artists'))
    df.createOrReplaceTempView("song_data_table")


def process_log_data(spark, input_data, output_data):
    """
    Loads data from the log data dataset, extracts columns to
    create users, time and songplays table and write the data as a
    parquet file to load into S3.

    Parameters
    spark: the spark session
    input_data: the folder where the log_data resides
    output_data: the folder where the parquet file are going to be stored.
    """

    # get filepath to log data file
    log_data = os.path.join(input_data, "log_data/*.json")

    # read log data file
    df = spark.read.json(log_data)

    # filter by actions for song plays
    df = df.filter(df.page == "NextSong").dropDuplicates()
    df.createOrReplaceTempView("log_data_table")

    # extract columns for users table
    users_table = df.select("userId", "firstName", "lastName",
                            "gender", "level").dropDuplicates()

    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(
        os.path.join(output_data, 'users'))

    # create timestamp column from original timestamp column
    get_timestamp = udf(
        lambda x: datetime.fromtimestamp(
            x / 1000), TimestampType())
    df = df.withColumn("timestamp", get_timestamp(col("ts")))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("start_time", get_datetime(df.ts))

    # creating columns for time table
    df = df.withColumn("hour", hour("timestamp"))
    df = df.withColumn("day", dayofmonth("timestamp"))
    df = df.withColumn("week", weekofyear("timestamp"))
    df = df.withColumn("month", month("timestamp"))
    df = df.withColumn("year", year("timestamp"))
    df = df.withColumn("weekday", dayofweek("timestamp"))

    # extract columns to create time table
    time_table = df.select("start_time", "hour", "day", "week",
                           "month", "year", "weekday").distinct()

    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month") \
        .mode('overwrite').parquet(os.path.join(output_data, 'time'))

    # read in song data to use for songplays table
    # song_df = spark.read.parquet(output_data+'songs/')

    # extract columns from joined song
    # and log datasets to create songplays table
    # Udacity Mentor Survesh helped with this
    # through Knowledge
    songplays_table = spark.sql("""
                                SELECT
                                monotonically_increasing_id() as songplay_id,
                                to_timestamp(logT.ts/1000) as start_time,
                                month(to_timestamp(logT.ts/1000)) as month,
                                year(to_timestamp(logT.ts/1000)) as year,
                                logT.userId as user_id,
                                logT.level as level,
                                songT.song_id as song_id,
                                songT.artist_id as artist_id,
                                logT.sessionId as session_id,
                                logT.location as location,
                                logT.userAgent as user_agent
                                FROM log_data_table logT
                                JOIN song_data_table songT
                                on logT.artist = songT.artist_name
                                and logT.song = songT.title
                            """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy("year", "month") \
                   .parquet(output_data+'songplays/')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://anju-udacity-dend/"
    # input_data = "data/"
    # output_data = "output/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
