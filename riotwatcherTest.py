from flask import Flask,request, jsonify
from riotwatcher import RiotWatcher, ApiError
import json 
import collections as cl
import pprint

watcher = RiotWatcher('')

my_region = 'jp1'
me = watcher.summoner.by_name(my_region, 'zer08823')
#print(me)

my_ranked_satatus = watcher.league.positions_by_summoner(my_region, me['id'])
#print(my_ranked_satatus)

#最新２０件の試合IDをlist化
recent_match_list = watcher.match.matchlist_by_account(my_region, me['accountId'],begin_index=0,end_index=20)

matches = recent_match_list['matches']
#print(matches[0]['gameId'])
gameId_list = []
seasonId_list = []
queueId_list = []
for i in range(20):
    gameId_list.append(matches[i]['gameId'])



#最近20試合のgameIdのリスト
print(gameId_list)

#試合毎のplayerIdを作成(固定)
match_plyerId_list = []
for i in range(10):
    match_plyerId_list.append("playerId" + str(i))


#一つの試合のデータをAPIから取得
match_data = watcher.match.by_id(my_region, gameId_list[0])
#pprint.pprint(match_data)
seasonId_list.append(match_data['seasonId'])
queueId_list.append(match_data['queueId'])
participants = match_data['participants']
#player一人のデータを取得
participants_data = participants[0]
#pprint.pprint(participants_data['stats'])
stats_data = participants_data['stats']



#jsonのplayerIdの情報
player_info_dict = {}
player_info_dict["teamId"] = participants_data['teamId']
player_info_dict["campionId"] = participants_data['championId']
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



print(player_info_dict)
#チーム0のデータを取得
#pprint.pprint(match_data['teams'][0])
#jsonのteam情報
team1_info_dict = {}
team1_info_dict["teamId"] = match_data['teams'][0]['teamId']
team1_info_dict["win"] = match_data['teams'][0]['win']
team1_info_dict["towerKills"] = match_data['teams'][0]['towerKills']
team1_info_dict["dragonKills"] = match_data['teams'][0]['dragonKills']
team1_info_dict["firstBaron"] = match_data['teams'][0]['firstBaron']
team1_info_dict["baronKills"] = match_data['teams'][0]['baronKills']
team1_info_dict["firstRiftHerald"] = match_data['teams'][0]['firstRiftHerald']
print(team1_info_dict)
team2_info_dict = {}
team2_info_dict["teamId"] = match_data['teams'][1]['teamId']
team2_info_dict["win"] = match_data['teams'][1]['win']
team2_info_dict["towerKills"] = match_data['teams'][1]['towerKills']
team2_info_dict["dragonKills"] = match_data['teams'][1]['dragonKills']
team2_info_dict["firstBaron"] = match_data['teams'][1]['firstBaron']
team2_info_dict["baronKills"] = match_data['teams'][1]['baronKills']
team2_info_dict["firstRiftHerald"] = match_data['teams'][1]['firstRiftHerald']
print(team2_info_dict)

#一つの試合の両方のチームデータを有する配列(要素数2)
both_team_data = []
both_team_data.append(team1_info_dict)
both_team_data.append(team2_info_dict)
print(both_team_data)

#一つのmatchのプレイヤーリスト
match_player_list = []
for i in range(10):
    participantIdnetities = (match_data['participantIdentities'])
    #pprint.pprint(participantIdnetities)
    player_data = participantIdnetities[i]
    player_data2 = player_data['player']
    #pprint.pprint(player_data2)
    match_player_list.append(player_data2['summonerName']) 
print(match_player_list)
print(match_plyerId_list)

example_player_dict = {}
example_player_dict[match_plyerId_list[0]] = player_info_dict
print(example_player_dict)

#for i in  range(9):
#    match_player_list = participants[i]

#jsonを作成
ys = cl.OrderedDict()
for i in range(len(gameId_list)):
    data = cl.OrderedDict()
    data["seasonId"] = seasonId_list[0]
    data["queueId"] = queueId_list[0]
    data["participantIdentities"] = example_player_dict
    #data["summonerName"] = match_player_list
    data["teams"] = both_team_data
    ys[gameId_list[i]] = data

print("{}".format(json.dumps(ys,indent=4)))
