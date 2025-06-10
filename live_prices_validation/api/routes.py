from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

@api.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    decision = data.get('decision')
    return jsonify({
        "status": "received",
        "your_decision": decision
    })

@api.route('/validate_prices', methods=['POST'])
def validate_prices():
    data = request.get_json()
    json_prices = data.get("prices")
    print(json_prices)
    return 'Ok', 200