from flask import Flask, render_template, redirect, url_for, request
import pandas as pd

import sys, os, os.path
sys.path.insert(0, os.path.abspath('..\src'))

from main import *
from credentials import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def input_track():
    text_input = request.form["track_uri"]

    try:
        sp_result = sp.track(text_input)
    except:
        print("This track does not exist, please enter a valid track uri")

    song_name = sp_result['name']
    song_link = sp_result['external_urls']['spotify']

    song_artist = sp_result['artists'][0]['name']
    artist_link = sp_result['artists'][0]['external_urls']['spotify']

    img_link = sp_result['album']['images'][0]['url']

    results = "You may enjoy these songs"
    
    try:
        results_df = main(text_input, 5)
    except:
        raise ValueError

    print("Searching for recommendations")

    results_df['link'] = results_df['uri'].apply(lambda x: sp.track(x)['external_urls']['spotify'])
    results_df.drop(columns='uri', inplace=True)

    full_list = results_df.values.tolist()

    return render_template("index.html", input_song = song_name, song_link = song_link,
        input_artist = song_artist, artist_link = artist_link,
        img_src = img_link,
        results_list = full_list,
        recommended_text=results, track_uri=text_input)

if __name__ == "__main__":
    app.run(host='localhost', port=8000)
