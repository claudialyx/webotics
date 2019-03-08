from app import app
from flask_cors import CORS
from flask import request, jsonify, make_response

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
# from webotics_api.blueprints.users.views import users_api_blueprint

@app.route('/_words', methods=['GET','POST'])
def words():
    if request.method == 'POST':
        data = request.get_json()
        json_data = data.get("text")
        if json_data:
            return make_response(jsonify("HI"))
    else:
        return make_response(jsonify("BYE"))
