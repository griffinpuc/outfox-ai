from flask import Flask
from flask import jsonify
from flask import request

import sys
sys.path.append('../')

import corematrix
import corescraper

import testAlgo
import json


app = Flask(__name__)
uf = open('usrdata.json',)
uData = json.load(uf)
gf = open('grpdata.json',)
gData = json.load(gf)


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
    pg = request.args['page']
    
    return corematrix.getUserRecsFromUser(int(userid), pg)


@app.route('/getRecGroups')
def getRecGroups(): 
    userid = request.args['userid']
    pg = request.args['page']

    return corematrix.getGroupRecsFromUser(int(userid), pg)

@app.route('/getRecResources')
def getRecResources():
    userid = request.args['userid']
    pg = request.args['page']

    return corematrix.getResourceRecsFromUser(int(userid), pg)

@app.route('/newResource')
def getNewResource():
    resource = request.args['resource']

    corescraper.consumeResourceId(resource)

@app.route('/updateGroup')
def getUpdateGroup():
    group = request.args['group']

    corescraper.updateGroup(group)

    return jsonify("true")

@app.route('/setUserTags')
def getSetUserTags():
    username = request.args['username']
    tag1 = request.args['t1']
    tag2 = request.args['t2']
    tag3 = request.args['t3']

    print(tag1 + ", " + tag2 + ", " + tag3, file=sys.stderr)

@app.route('/getUserPgs')
def getUserPgs():
    userid = request.args['userid']
    return jsonify({"test": "userData", "userid":str(userid)})


@app.route('/getGroupPgs')
def getGroupPgs():
    userid = request.args['userid']
    return jsonify({"test": "userData", "userid":str(userid)})


@app.route('/getResourcePgs')
def getResourcePgs():
    userid = request.args['userid']
    return jsonify({"test": "userData", "userid":str(userid)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)