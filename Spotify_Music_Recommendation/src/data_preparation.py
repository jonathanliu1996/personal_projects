from pyspark.sql.types import StringType, StructField, StructType
from pyspark.sql.functions import split
from pyspark.sql import functions as F

import os

def json_directory(dir):
    '''
    Get the full path for each json file in a folder
        Input: Directory containing json files
        Output: List of full path
    '''
    files_path = []
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            files_path.append(full_path)

    return files_path


def read_all_json(json_file, spark):
    """
    Read each json files to and consolidate into one Spark DataFrame (with optional parquet file)
        Input: Json file
        Output: Consolidated Spark DataFrame (optional .parquet file)
    """
    global parquet_df
    spark_df = spark.read.json(json_file, multiLine = True)
    
    explode_playlists = spark_df.withColumn("exploded", F.explode("playlists"))

    playlists = explode_playlists.withColumn("playlists_tracks", F.col('exploded').getItem('tracks'))

    playlists_tracks = playlists.select('playlists_tracks')
    
    track_uri = playlists_tracks.withColumn("track_uri_exploded", F.col('playlists_tracks').getItem("track_uri"))

    # Pyspark dataframe error due to maxresultsize error, utilizing Pandas dataframe for this situation
    # uri_list = [row[0] for row in track_uri.select('track_uri_exploded').collect()]
    pandasDF = track_uri.toPandas()
    uri_list = pandasDF['track_uri_exploded'].tolist()

    flat_list = [item for sublist in uri_list for item in sublist]
    
    parquet_loop = spark.createDataFrame(flat_list, StringType())
    parquet_df = parquet_df.union(parquet_loop)

    return parquet_df


def combine_json(files_path, spark):
    global parquet_df
    parquet_df = spark.createDataFrame([], StringType())

    for json_file in files_path:
        read_all_json(json_file, spark)

    return parquet_df


def get_track_uri(parquet_df, spark):
    '''
    Read parquet file in directory, and extract the 'track_uri'
        Input: Parquet file
        Output: Dataframe for 'track_uri'
    '''
    parquet_schema = StructType([
        StructField('track_uri', StringType(), True)
    ])

    track_uri_df = spark.createDataFrame([], parquet_schema)
    track_uri_df = parquet_df.withColumn("track_uri_only", split(parquet_df['value'], ':').getItem(2)).select("track_uri_only")

    return track_uri_df


def get_distinct_track_uri(track_uri_df):
    distinct_tracks = track_uri_df.distinct()
    
    return distinct_tracks
    # distinct_tracks.write.parquet("distinct_tracks.parquet")