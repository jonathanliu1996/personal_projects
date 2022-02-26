from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import matplotlib.pyplot as plt

def convert_to_vector(audio_features):
    # Convert features to vector
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

    assembled_data=assemble.transform(audio_features)

    return assembled_data


def scale_data(assembled_data):
    # Scale data
    scale = StandardScaler(inputCol = 'features', outputCol = 'standardized')

    data_scale = scale.fit(assembled_data)
    data_scale_output = data_scale.transform(assembled_data)

    return data_scale_output

    
def find_optimal_k(data_scale_output):
    # Find optimal clusters based on silhouette score (Optimal result k=9)
    silhouette_score = []

    evaluator = ClusteringEvaluator(predictionCol = 'prediction', featuresCol = 'standardized', metricName = 'silhouette',
                                   distanceMeasure = 'squaredEuclidean')

    for i in range (2, 15):
        KMeans_algo = KMeans(featuresCol = 'standardized', k = i)
        
        KMeans_fit = KMeans_algo.fit(data_scale_output)
        
        output = KMeans_fit.transform(data_scale_output)
        
        score = evaluator.evaluate(output)
        silhouette_score.append(score)

    fig, ax = plt.subplots(1,1, figsize =(8,6))
    ax.plot(range(2,15),silhouette_score)
    ax.set_xlabel('k')
    ax.set_ylabel('cost')
    plt.show()


def model_fitting(data_scale_output, k_clusters):  
    KMeans_algo = KMeans(featuresCol = 'standardized', k = k_clusters)
        
    KMeans_fit = KMeans_algo.fit(data_scale_output)
        
    prediction_df = KMeans_fit.transform(data_scale_output)

    # save KMeans model
    # KMeans_fit.write().overwrite().save("kmeans_model")

    # save cluster labeling for all tracks
    # prediction_df.write.format("parquet").mode("overwrite").save("predictions_track.parquet")

    return prediction_df