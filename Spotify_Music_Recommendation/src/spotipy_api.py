import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from pyspark.sql.types import StructType, StructField, StringType, DecimalType
from pyspark.sql.functions import col

import math
import numpy as np


def spotipy_credentials(cid, secret):

    client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

    return sp


def get_audio_features(distinct_tracks, sp, spark):

    # Return audio features for track_uri 
    audio_features_schema = StructType([
        StructField("danceability", StringType()),
        StructField("energy", StringType()),
        StructField("key", StringType()),
        StructField("loudness", StringType()),
        StructField("mode", StringType()),
        StructField("speechiness", StringType()),
        StructField("acousticness", StringType()),
        StructField("instrumentalness", StringType()),
        StructField("liveness", StringType()),
        StructField("valence", StringType()),
        StructField("tempo", StringType()),
        StructField("time_signature", StringType()),
        StructField("uri", StringType())
    ])

    audio_features = spark.createDataFrame([], schema=audio_features_schema)

    uri_list = [row[0] for row in distinct_tracks.select('track_uri_only').collect()]
    front_track = "spotify:track:"
    uri_list_ready = [front_track + uri for uri in uri_list]

    # # Split the list into multiple arrays, each with 100 track uri
    number_of_arrays = math.ceil(len(uri_list_ready)/ 100)
    split_list = np.array_split(uri_list_ready, number_of_arrays)


    # All datasets, commented out and testing with first item in split_list
    # for row in split_list:    
    #     clean_list = list(filter(None, sp.audio_features(row)))
    #     spark_df_loop = spark.createDataFrame(clean_list, schema = audio_features_schema)
    #     audio_features = audio_features.union(spark_df_loop)

    # Testing dataset with single list, split_list[0]
    clean_list = list(filter(None, sp.audio_features(split_list[0])))
    audio_features = spark.createDataFrame(clean_list, schema = audio_features_schema)


    # Convert string columns to Decimal Type
    audio_features = audio_features.withColumn("danceability", col("danceability").cast(DecimalType(10,5))) \
                            .withColumn("energy", col("energy").cast(DecimalType(10,5))) \
                            .withColumn("key", col("key").cast(DecimalType(10,5))) \
                            .withColumn("loudness", col("loudness").cast(DecimalType(10,5))) \
                            .withColumn("mode", col("mode").cast(DecimalType(10,5))) \
                            .withColumn("speechiness", col("speechiness").cast(DecimalType(10,5))) \
                            .withColumn("acousticness", col("acousticness").cast(DecimalType(10,5))) \
                            .withColumn("instrumentalness", col("instrumentalness").cast(DecimalType(10,5))) \
                            .withColumn("liveness", col("liveness").cast(DecimalType(10,5))) \
                            .withColumn("valence", col("valence").cast(DecimalType(10,5))) \
                            .withColumn("tempo", col("tempo").cast(DecimalType(10,5))) \
                            .withColumn("time_signature", col("time_signature").cast(DecimalType(10,5))) \
                            .withColumn("uri", col("uri"))

    return audio_features