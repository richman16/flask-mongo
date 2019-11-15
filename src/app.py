# import pymongo
import json
from flask import Flask, jsonify, make_response, request
from pymongo import MongoClient
from bson import json_util, ObjectId

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
def get_authors():
    authors = db.authors.find()
    return jsonify({
        'data': json.loads(json_util.dumps(authors))
    })

@app.route('/api/author/', methods=['POST'])
def create_author():
    if not request.json or not 'name' in request.json or not 'bio' in request.json:
        return jsonify({ 'code': 400, 'message': 'Bad request' }), 400

    name = request.json['name']
    bio = request.json['bio']

    db.authors.insert({ 'name': name,'bio': bio })
    return jsonify(), 201


# @app.route('/api/author', methods=['POST'])
# def create_author():
#     # print request.json
#     if not request.json or not 'name' in request.json or not 'bio' in request.json:
#         # Requiere --> from flask import abort
#         # abort(400)
#         return jsonify( {
#             'code': 400,
#             'message': 'Bad request'
#         } ), 400

#     #   CONNECT and INSERT to BD
#     author = db.authors.insert_one(request.json).inserted_id
#     # print author
#     cosa = db.authors.find_one( {"_id": ObjectId(author)} )
#     print type(cosa["name"])

#     return db.authors.find_one( {"_id": ObjectId(author)} )
#     # return jsonify({
#     #     author: cosa["name"]
#     # })


@app.route('/api/author/<string:author_id>', methods=['GET'])
def find_author(author_id):
    # Especificar que hacer si no hay un author
    if not author_id:
        return jsonify( {
            'code': 400,
            'message': 'Bad request'
        } ), 400
    author = db.authors.find_one( {"_id": ObjectId(author_id)} )
    print author
    return jsonify(json.loads(json_util.dumps(author)))

@app.route('/api/author/<author_id>', methods=['PUT'])
def update_author(author_id):
    name = request.json["name"]
    bio = request.json["bio"]

    db.authors.update( { '_id': ObjectId(author_id) }, {
        '$set': {
            'name': name,
            'bio': bio
        }
    } )
    return jsonify(), 200


@app.route('/api/author/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    # Especificar que hacer si no hay un author
    if not author_id:
        return jsonify( {
            'code': 400,
            'message': 'Bad request'
        } ), 400
    result = db.authors.delete_one( { '_id': ObjectId(author_id) } )
    #   Tambien se puede utilizar la siguiente linea
    #   db.authors.remove( { '_id': ObjectId(author_id) } )
    print result.deleted_count
    return jsonify(), 200


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