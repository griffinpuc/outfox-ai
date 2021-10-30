from flask import jsonify

def giveData(userID):
	return jsonify({"UserId": str(userID)})