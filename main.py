from dotenv.main import load_dotenv
import requests
import json
import smtplib
import ssl
import os
#import socks

load_dotenv()

headers =   {
        'user_agent':os.environ['USER_AGENT']
            }

# Weekly Songs Chart
songs_payload = {
        'api_key':os.environ['API_KEY'],
        'user':os.environ['LASTFM_USERNAME'],
        'method':'user.getTopTracks',
        'period':'7day',
        'limit':'10',
        'format':'json'
                }
r_songs = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=songs_payload)
songs_json = r_songs.json()
songs_ranking = ""

# Songs Ranking System
for i in range(10):
    songs_ranking = songs_ranking + f"{songs_json['toptracks']['track'][i]['@attr']['rank']}. {songs_json['toptracks']['track'][i]['name']} by {songs_json['toptracks']['track'][i]['artist']['name']}. ({songs_json['toptracks']['track'][i]['playcount']} Scrobbles.)\n"

# Weekly Albums Chart
albums_payload =    {
        'api_key': os.environ['API_KEY'],
        'user': os.environ['LASTFM_USERNAME'],
        'method':'user.getTopAlbums',
        'period':'7day',
        'limit':'10',
        'format':'json'
                    }
r_albums = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=albums_payload)
albums_json = r_albums.json()
albums_ranking = ""

# Albums Ranking System
for i in range(10):
     albums_ranking = albums_ranking + f"{albums_json['topalbums']['album'][i]['@attr']['rank']}. {albums_json['topalbums']['album'][i]['name']} by {albums_json['topalbums']['album'][i]['artist']['name']}. ({albums_json['topalbums']['album'][i]['playcount']} Scrobbles.)\n"

# Weekly Artists Chart
artists_payload =   {
        'api_key':os.environ['API_KEY'],
        'user':os.environ['LASTFM_USERNAME'],
        'method':'user.getTopArtists',
        'period':'7day',
        'limit':'10',
        'format':'json'
                    }
r_artists = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=artists_payload)
artists_json = r_artists.json()
artists_ranking = ""

# Artists Ranking System
for i in range(10):
    artists_ranking = artists_ranking + f"{artists_json['topartists']['artist'][i]['@attr']['rank']}. {artists_json['topartists']['artist'][i]['name']}. ({artists_json['topartists']['artist'][i]['playcount']} Scrobbles.)\n"

# Message to-send
message = f'''\
Subject : Last Week Music Listening Status


Hello, here is the summary of what you listened to this week! I hope you enjoyed it all  :D

- Top Songs of the week:
{songs_ranking}
- Top Albums of the week:
{albums_ranking}
- Top Artists of the week:
{artists_ranking}
Made by: adnanekouna-a
'''
# Email Sending
server_name = os.environ['SERVER_NAME']
port = int(os.environ['SERVER_PORT'])
sender = os.environ['SENDER_EMAIL']
password = os.environ['SENDER_PASSWORD']
receiver = os.environ['RECEIVER_EMAIL']
context = ssl.create_default_context()

# # Make the SMTP library go through a proxy (the only way to make it work in PythonAnywhere)
# proxy_host = "proxy.server"
# proxy_port = 3128
# socks.setdefaultproxy(socks.HTTP, proxy_host, proxy_port)
# socks.wrapmodule(smtplib)

with smtplib.SMTP_SSL(server_name, port, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender,receiver, message.encode('utf-8'))
