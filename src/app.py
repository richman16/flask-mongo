# import pymongo
from flask import Flask, jsonify, make_response, request
from pymongo import MongoClient
from bson.objectid import ObjectId

#   Creating application
app = Flask(__name__)

#   MongoDB connection
client = MongoClient('mongodb://db:27017')
db = client.libraries

#   GET /api/
@app.route('/api/', methods=['GET'])
def get_root():
    return jsonify( {
        'message': 'Welcome to the jungle!'
    } )

@app.route('/api/author', methods=['GET'])


@app.route('/api/author', methods=['POST'])
def create_author():
    # print request.json
    if not request.json or not 'name' in request.json or not 'bio' in request.json:
        # Requiere --> from flask import abort
        # abort(400)
        return jsonify( {
            'code': 400,
            'message': 'Bad request'
        } ), 400

    #   CONNECT and INSERT to BD
    author = db.authors.insert_one(request.json).inserted_id
    # print author
    cosa = db.authors.find_one( {"_id": ObjectId(author)} )
    print type(cosa["name"])

    return db.authors.find_one( {"_id": ObjectId(author)} )
    # return jsonify({
    #     author: cosa["name"]
    # })

#   Error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {
        'code': 404,
        'message': 'Not found'
    } ), 404)

#   Run application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)