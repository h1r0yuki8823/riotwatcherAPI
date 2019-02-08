from flask import Flask, request, jsonify, make_response
from riotwatcher import RiotWatcher, ApiError
import json
import collections as cl 
import pprint 
import settings

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #JSONの日本語文字化け対策

API_KEY = settings.AP

watcher = RiotWatcher(API_KEY)
default_region = 'jp1'

@app.route('/get/summonerinfo/<id>', methods=['GET'])
def get_summonerInfo(id):
    your_summonerId = id
    if request.method == 'GET':
        summoner_info = watcher.summoner.by_name(default_region,your_summonerId)
        return make_response(jsonify(summoner_info))


app.run(host="127.0.0.1", port=5000)