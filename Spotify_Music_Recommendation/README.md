End-to-end project created to recommend Spotify songs based on an input track uri

Full project utilized the 'Million Playlist' dataset provided by Spotify here:
    https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

Src here contains only 2 playlists

By inputting a track uri from Spotify (found in the URL), a K-means machine learning model provides a list of 5 song recommendations.
Recommendations and calculations are based on Audio Featrures (provided by Spotify's API) and the shortest Euclidean distance

Tools utilized include:
- PySpark
- Pandas
- Flask
- HTML
- CSS

