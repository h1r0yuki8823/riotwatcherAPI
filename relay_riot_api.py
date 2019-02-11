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

@app.route('/get/test_info/<id>', methods=['GET'])
def test_get(id):
    test_summonerId = id 
    if request.method == 'GET':
        test_info = watcher.summoner.by_name(default_region, test_summonerId)

       #最新の試合データ20件を取得
        ts_recent_match_list = watcher.match.matchlist_by_account(default_region, test_info['accountId'],begin_index=0, end_index=20)
        ts_matches = ts_recent_match_list['matches']
        
        return make_response(jsonify(test_info))


@app.route('/get/games_info/<id>', methods=['GET'])
def get_summonerInfo(id):
    gameId_list = []
    seasonId_list = []
    queueId_list = []
    #試合毎のplayerIDを作成（固定）
    match_playerId_list = ["playerId0","playerId1","playerId2","playerId3","playerId4","playerId5","playerId6","playerId7","playerId8","playerId9",]
    your_summonerId = id
    if request.method == 'GET':
        summoner_info = watcher.summoner.by_name(default_region,your_summonerId)
        print(summoner_info)
        #最新20件の試合IDをlist化
        recent_match_list = watcher.match.matchlist_by_account(default_region, summoner_info['accountId'],begin_index=0, end_index=20)
        #print(recent_match_list)
        matches = recent_match_list['matches']
        for i in range(20):
            gameId_list.append(matches[i]['gameId'])

        print(gameId_list)
        #返すjsonファイルを作成
        #for i in range(len(gameId_list)):
        for i in range(1):
            match_data = watcher.match.by_id(default_region, gameId_list[i])
            
        print(match_data)
        
        return 

        
        #json形式でreturn
        #return make_response(jsonify(match_data))


app.run(host="127.0.0.1", port=5000)