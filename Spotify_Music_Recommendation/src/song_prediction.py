from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import StandardScalerModel, VectorAssembler
from pyspark.sql.types import StructType, StructField, StringType, DecimalType
from pyspark.sql.functions import col, expr
from pyspark.ml.functions import vector_to_array
from pyspark.sql import functions as F
from pathlib import Path

def label_new_song(input_track_uri, modelPath, scalePath, sp, spark):
    assemble = VectorAssembler(inputCols=[
    'danceability',
    'key',
    'loudness',
    'mode',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'time_signature',
    'energy'], outputCol='features'
    )

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

    persistedModel = KMeansModel.load(modelPath)
    scaleModel = StandardScalerModel.load(scalePath)

    new_input_song = spark.createDataFrame(sp.audio_features("spotify:track:" + input_track_uri), schema = audio_features_schema)

    converted_input_song = new_input_song.withColumn("danceability", col("danceability").cast(DecimalType(10,5))) \
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

    input_assembled_data = assemble.transform(converted_input_song)

    clustered_input_song = scaleModel.transform(input_assembled_data)

    input_song_cluster = persistedModel.transform(clustered_input_song)

    return input_song_cluster


def input_cluster_comparison(input_song_cluster, number_of_recommendations, sp, spark):  
    input_cluster_prediction = input_song_cluster.select("prediction").collect()[0][0]
    print("This song belongs to cluster: " + str(input_cluster_prediction))

    if input_cluster_prediction == 0:
        # cluster0: 309,979
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_0.parquet"
    elif input_cluster_prediction == 1:
        # cluster1: 51,788
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_1.parquet"
    elif input_cluster_prediction == 2:
        # cluster2: 448,387
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_2.parquet"
    elif input_cluster_prediction == 3:
        # cluster3: 143,409
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_3.parquet"
    elif input_cluster_prediction == 4:
        # cluster4: 391,959
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_4.parquet"
    elif input_cluster_prediction == 5:
        # cluster5: 217,946
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_5.parquet"
    elif input_cluster_prediction == 6:
        # cluster6: 304,968
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_6.parquet"
    elif input_cluster_prediction == 7:
        # cluster7: 264,355
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_7.parquet"
    elif input_cluster_prediction == 8:
        # cluster8: 129,399
        cluster_path = str(Path(__file__).parent.parent) + "\\track_uri_clusters\\cluster_8.parquet"
    else:
        print("Unable to find any recommendations for this track, please choose another track")

    cluster_parquet = spark.read.parquet(cluster_path)

    input_features_standardized = input_song_cluster.select("standardized").collect()[0][0].tolist()
    # input_features_standardized

    comparison_df = cluster_parquet.withColumn("input_song_features", F.array([F.lit(x) for x in input_features_standardized]))

    comparison_df = comparison_df.withColumn("standardized", vector_to_array("standardized"))

    comparison_df = comparison_df.withColumn("column_difference",
                                expr("transform(arrays_zip(standardized, input_song_features), \
                                x -> (x.standardized - x.input_song_features) * (x.standardized - x.input_song_features))"))
 
    comparison_df = comparison_df.withColumn("sum_col_distance",
                                expr("aggregate(column_difference, DOUBLE(0), (acc, x) -> acc + x)"))

    top_predictions = comparison_df.filter(col('sum_col_distance') != 0).sort("sum_col_distance")
    top_x_predictions = top_predictions.limit(number_of_recommendations)

    df_pandas = top_x_predictions.toPandas()
    df_pandas = df_pandas[['uri', 'sum_col_distance']]

    df_pandas['Artist'] = df_pandas['uri'].apply(lambda x: sp.track(x)['artists'][0]['name'])
    df_pandas['Song Name'] = df_pandas['uri'].apply(lambda x: sp.track(x)['name'])

    return df_pandas