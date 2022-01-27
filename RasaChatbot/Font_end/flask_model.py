from flask import Flask, render_template, request, jsonify
import os, sys, requests, json
from random import randint

# Initialization Flask
app = Flask(__name__, template_folder='templates')
context_set = ""

# Config upload folder
# app.config['UPLOAD_FOLDER'] = "static"


# Process requests
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        val = str(request.args.get('text'))
        print(val)
        if val is not None:
            pass
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        res = res.json()
        val = res[0]['text']
        return render_template('index.html', val=val)


# Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
