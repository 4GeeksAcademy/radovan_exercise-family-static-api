"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"error": "member not found"}), 400


    return jsonify(member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(member_id)
    if member["done"]== False:
        return jsonify({"error": "member not found"}), 400


    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_new_member():
    body= request.json
    first_name= body.get("first_name", None)
    age= body.get("age", None)
    lucky_numbers= body.get("lucky_numbers", None)
    id= body.get("id", None)
    if not first_name or not age or not lucky_numbers:
        return jsonify({"error":"misssing fields"}), 400
    # if id is not None 

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.add_member(body)
    print(member)
        


    return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
