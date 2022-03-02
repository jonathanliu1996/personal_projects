End-to-end project created to recommend Spotify songs based on an input track uri

Full project utilized the 'Million Playlist' dataset provided by Spotify at this link:
    https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

Src here contains only 2 playlists

Project has been deployed on Heroku - note that due to slug size limit on the platform, a few clusters had to be removed to ensure deployment
Source code here may provide different recommendations compared to the algorithm deployed on Heroku
    http://recommendedsongs.herokuapp.com/


By inputting a track uri from Spotify (found in the URL), a K-means machine learning model provides a list of 5 song recommendations.
Recommendations and calculations are based on Audio Featrures (provided by Spotify's API) and the shortest Euclidean distance

Parquet files have been included for clustering and song recommendation

Tools utilized include:
- PySpark
- Pandas
- Flask
- HTML
- CSS

