from flask import Flask, request, jsonify
from riotwatcher import RiotWatcher, ApiError
import json
import collections as cl 
import pprint 
import settings

API_KEY = settings.AP

watcher = RiotWatcher(API_KEY)
my_region = 'jp1'
me = watcher.summoner.by_name(my_region, 'zer08823')
print(me)

