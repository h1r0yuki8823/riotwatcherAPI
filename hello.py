from flask import Flask,request, jsonify
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['POST'])
def post_json():
    json = request.get_json()
    return jsonify(json)

@app.route('/', methods=['GET'])
def get_json_from_dictionary():
    dic = {
        'foo': 'bar',
        'ほげ': 'ふが' 
    }
    return jsonify(dic)