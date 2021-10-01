from flask import Flask
from flask import jsonify
from flask import request
import testAlgo
app = Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])

def welcome():
    return "Hello World!"

@app.route('/person/')
def hello():
    return jsonify({'name':'Jimit',
                    'address':'India'})

#@app.route("/returnRelated"):
    # talk to reccommendation engine and return json


@app.route('/returnExploreRecords')
def getExploreRecords():
    userid = request.args['userID']

    return testAlgo.giveData(userid)




@app.route('/getRecUsers')
def getRecUsers():
    userid = request.args['userid']
    return jsonify({"test": "userData"})


@app.route('/getRecGroups')
def getRecGroups():
    userid = request.args['userid']
    return jsonify({"test": "groupData"})


@app.route('/getRecResources')
def getRecResources():
    userid = request.args['userid']
    return jsonify({"test": "resourceData"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)