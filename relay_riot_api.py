from flask import Flask, request, jsonify, make_response
from riotwatcher import RiotWatcher, ApiError
from flask_cors import CORS 
import json
import collections as cl 
import pprint 
import api_key
import os 

#実行する FLASK_APP=relay_riot_api.py flask run

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False #JSONの日本語文字化け対策

API_KEY = api_key.RIOT_API_KEY

watcher = RiotWatcher(API_KEY)
default_region = 'jp1'

champion_dict = {}
with open('champion.json', encoding="utf-8") as f:
    df = json.load(f)
for i in df["data"]:
    champion_dict[int(df["data"][i]["key"])] = [df["data"][i]["name"]]

print(champion_dict)

#テスト用
@app.route('/get/test_info/<id>', methods=['GET'])
def test_get(id):
    test_summonerId = id 
    if request.method == 'GET':
        test_info = watcher.summoner.by_name(default_region, test_summonerId)

       #最新の試合データ20件を取得
        ts_recent_match_list = watcher.match.matchlist_by_account(default_region, test_info['accountId'],begin_index=0, end_index=20)
        ts_matches = ts_recent_match_list['matches']
        
        return make_response(jsonify(test_info))

#プレイヤー情報を取得
@app.route('/get/user_info/<id>', methods=['GET'])
def get_summonerInfo(id):
    summonerId = id 
    if request.method == 'GET':
        summoner_info = watcher.summoner.by_name(default_region, summonerId)
        return make_response(jsonify(summoner_info))


#試合情報を取得
@app.route('/get/games_info/<id>', methods=['GET'])
def get_gamesInfo(id):
    participantId_list  = []
    gameId_list = []
    ys = cl.OrderedDict()
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
        for i in range(10):
            gameId_list.append(matches[i]['gameId'])
            participantId_list.append('participantId' + str(i))
        print(gameId_list)
        #返すjsonファイルを作成
        #for i in range(len(gameId_list)):
        for i in range(10):

            match_data = watcher.match.by_id(default_region, gameId_list[i])
            #seasonId_list.append(match_data['seasonId'])
            #queueId_list.append(match_data['queueId'])
            participants = match_data['participants']
            participantIdentities = match_data['participantIdentities']
            #変数dataに一つの試合データjsonを追加していく
            data = cl.OrderedDict()
            #一つの試合の10プレイヤー分の情報を持った辞書
            match_player_dict = {}
            #一つの試合の両チーム毎のデータ
            team1_info_dict = {}
            team2_info_dict = {}
            #上記の辞書を一つのリストに
            both_team_data = []
            
            #一つの試合の10プレイヤー分のデータを作る処理
            for j in range(10):
                participants_data = participants[j]
                player_info_dict = {}
                player_info_dict['summonerName'] = participantIdentities[j]['player']['summonerName']
                player_info_dict["teamId"] = participants_data['teamId']
                player_info_dict["championId"] = participants_data['championId']
                player_info_dict["championName"] = champion_dict[participants_data['championId']]
                print(champion_dict[participants_data['championId']])
                player_info_dict["spell1Id"] = participants_data['spell1Id']
                player_info_dict["spell2Id"] = participants_data['spell2Id']
                player_info_dict["champLevel"] = participants_data['stats']['champLevel']
                player_info_dict["perk0"] = participants_data['stats']['perk0']
                player_info_dict["perk1"] = participants_data['stats']['perk1']
                player_info_dict["perk2"] = participants_data['stats']['perk2']
                player_info_dict["perk3"] = participants_data['stats']['perk3']
                player_info_dict["perk4"] = participants_data['stats']['perk4']
                player_info_dict["perk5"] = participants_data['stats']['perk5']
                player_info_dict["item0"] = participants_data['stats']['item0']
                player_info_dict["item1"] = participants_data['stats']['item1']
                player_info_dict["item2"] = participants_data['stats']['item2']
                player_info_dict["item3"] = participants_data['stats']['item3']
                player_info_dict["item4"] = participants_data['stats']['item4']
                player_info_dict["item5"] = participants_data['stats']['item5']
                player_info_dict["item6"] = participants_data['stats']['item6']
                player_info_dict["totalDamegeTaken"] = participants_data['stats']['totalDamageTaken']
                player_info_dict["kills"] = participants_data['stats']['kills']
                player_info_dict["deaths"] = participants_data['stats']['deaths']
                player_info_dict["assists"] = participants_data['stats']['assists']
                player_info_dict["wardsPlaced"] = participants_data['stats']['wardsPlaced']
                player_info_dict["doubleKills"] = participants_data['stats']['doubleKills']
                player_info_dict["tripleKills"] = participants_data['stats']['tripleKills']
                player_info_dict["quadraKills"] = participants_data['stats']['quadraKills']
                player_info_dict["totalMinionsKilled"] = participants_data['stats']['totalMinionsKilled']

                
                match_player_dict[match_playerId_list[j]] = player_info_dict

            #teamデータを作成
            team1_info_dict['teamId'] = match_data['teams'][0]['teamId']
            team1_info_dict["win"] = match_data['teams'][0]['win']
            team1_info_dict["towerKills"] = match_data['teams'][0]['towerKills']
            team1_info_dict["dragonKills"] = match_data['teams'][0]['dragonKills']
            team1_info_dict["firstBaron"] = match_data['teams'][0]['firstBaron']
            team1_info_dict["baronKills"] = match_data['teams'][0]['baronKills']
            team1_info_dict["firstRiftHerald"] = match_data['teams'][0]['firstRiftHerald']
            
            
            team2_info_dict["teamId"] = match_data['teams'][1]['teamId']
            team2_info_dict["win"] = match_data['teams'][1]['win']
            team2_info_dict["towerKills"] = match_data['teams'][1]['towerKills']
            team2_info_dict["dragonKills"] = match_data['teams'][1]['dragonKills']
            team2_info_dict["firstBaron"] = match_data['teams'][1]['firstBaron']
            team2_info_dict["baronKills"] = match_data['teams'][1]['baronKills']
            team2_info_dict["firstRiftHerald"] = match_data['teams'][1]['firstRiftHerald']
           

            both_team_data.append(team1_info_dict)
            both_team_data.append(team2_info_dict)
            

            data['seasonId'] = match_data['seasonId']
            data['queueId'] = match_data['queueId']
            data['paticipantIdentities'] = match_player_dict
            data['teams'] = both_team_data
            data['gameId'] = gameId_list[i]
            print(str(i))
            ys[i] = data

         
        #json形式でreturn
        #return make_response(jsonify(match_data))
        return make_response(jsonify(ys))

#app.run(host="127.0.0.1", port=5000)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)