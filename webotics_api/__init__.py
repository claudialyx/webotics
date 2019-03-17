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
    if (request.method == "POST"):
        posted_data = request.get_json()
        # json_data = data.get("text")
        if posted_data:
            string_data = posted_data.get('data')
            # send to brain
            processed_data = return_matches(string_data)
            return jsonify(processed_data)
    else:
        with open(os.path.join(os.path.dirname(__file__), "../web_scraper", "data.json")) as file:
            data = json.load(file)
            return jsonify(data)
