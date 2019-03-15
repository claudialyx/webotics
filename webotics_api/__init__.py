from app import app
from flask_cors import CORS
from flask import request, jsonify, make_response
import json, os
from NLP.test import return_matches

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
# from webotics_api.blueprints.users.views import users_api_blueprint
        
j = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data.json')

@app.route('/_words', methods=['GET','POST'])
def words():
    posted_data = request.get_json()
    # json_data = data.get("text")
    string_data = posted_data.get('data')
    # send to brain
    processed_data = return_matches(string_data)
    return jsonify(processed_data)
