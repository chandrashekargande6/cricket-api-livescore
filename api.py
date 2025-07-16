import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import get_all_live_matches, get_match_scorecard

app = Flask(__name__)
CORS(app)

@app.route('/api/livematches', methods=['GET'])
def live_matches():
    return jsonify(get_all_live_matches())

@app.route('/api/match', methods=['GET'])
def match_details():
    match_url = request.args.get("url")
    if not match_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    if "live-cricket-scores" in match_url:
        match_url = match_url.replace("live-cricket-scores", "live-cricket-scorecard")
    return jsonify(get_match_scorecard(match_url))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
