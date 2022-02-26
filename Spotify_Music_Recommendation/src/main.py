from pyspark.sql import SparkSession

import sys
import os

from src.data_preparation import json_directory, combine_json, get_track_uri, get_distinct_track_uri
from src.spotipy_api import spotipy_credentials, get_audio_features
from src.kmeans_model import convert_to_vector, scale_data, find_optimal_k, model_fitting
from src.song_prediction import label_new_song, input_cluster_comparison
from src.credentials import cid, secret

from pathlib import Path


def processing_dataset():
    '''
    Processing json files in dataset folder, files will be combined and distinct tracks extracted
        Input: json file path
        Output: 'distinct_tracks' dataframe containing list of unique tracks
    '''
    print("Reading json files and extracting track uri")

    parquet_df = combine_json(files_path, spark)
    track_uri_df = get_track_uri(parquet_df, spark)
    distinct_tracks = get_distinct_track_uri(track_uri_df)
    return distinct_tracks



def connect_to_spotify_api(cid, secret):
    '''
    Connect to Spotify API using spotipy
        Input: Client ID and Secret ID
        Output: spotipy.sp function
    '''
    print("Connecting to Spotify API")
    
    return spotipy_credentials(cid, secret)


def audio_feature_extraction(distinct_tracks, sp):
    '''
    Retreive audio feature for each track from Spotify's API
        Input: Dataframe of unique tracks
        Output: 'audio_features' dataframe containing audio features for each track
    '''
    print("Retreiving audio features from Spotify")

    audio_features = get_audio_features(distinct_tracks, sp, spark)
    return audio_features


def building_model():
    '''
    Scale the features and use K-means to determine cluster for each track
        Output: 'prediction_df' dataframe containing cluster label
    '''
    assembled_data = convert_to_vector(audio_features)
    data_scale_output = scale_data(assembled_data)

    # Calculate and display silhouette score for k-clusters from 2-15 (optimal k=9)
    # find_optimal_k(data_scale_output)

    prediction_df = model_fitting(data_scale_output, 9)
    return prediction_df


def recommend_song(input_track_uri, modelPath, scalePath, number_of_recommendations, sp, spark):
    input_song_cluster = label_new_song(input_track_uri, modelPath, scalePath, sp, spark)

    recommendation_df = input_cluster_comparison(input_song_cluster, number_of_recommendations, sp, spark)
    return recommendation_df


def main(input_track_uri, number_of_recommendations):

    input_track_uri = input_track_uri
    number_of_recommendations = number_of_recommendations

    from src.credentials import cid, secret

    spark = SparkSession.builder.appName('Spotify_Music_Recomendation').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    path = os.getcwd()

    # Path to dataset
    # dataset_path = parent + "\\dataset"
    # files_path = json_directory(dataset_path)

    # Spotify API: Input Client ID and Secret ID
    cid = cid
    secret = secret

    # Spotify: Input track uri for similar song recommendations

    # Path to kmeansModel and scaleModel
    modelPath = ".\\kmeans_model"
    scalePath = ".\\standardized_scale"

    # Input number of requested song recommendations
    # number_of_recommendations = 10

    sp = connect_to_spotify_api(cid, secret)

    # Below 3 lines used to pre-process the data and build k-means model
    # distinct_tracks = processing_dataset()
    # audio_features = audio_feature_extraction(distinct_tracks, sp)
    # prediction_df = building_model()


    recommendation_df = recommend_song(input_track_uri, modelPath, scalePath, number_of_recommendations, sp, spark)

    print("Based on your chosen song, we think that you may enjoy these:")
    # print(recommendation_df[['Artist', 'Song Name', 'uri']])
    return recommendation_df[['Artist', 'Song Name', 'uri']]