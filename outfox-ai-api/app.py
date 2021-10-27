from flask import Flask
from flask import jsonify
from flask import request

import sys
sys.path.append('../')

import corematrix

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
    return jsonify(uData)#PUT MY DATA HERE


@app.route('/getRecGroups')
def getRecGroups():
    userid = request.args['userid']
    pg = request.args['page']

    return corematrix.getGroupRecsFromUser(userid)



@app.route('/getRecResources')
def getRecResources():
    userid = request.args['userid']
    pg = request.args['page']
    return jsonify({"test": "userData", "userid":str(userid), "page": str(pg)})



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