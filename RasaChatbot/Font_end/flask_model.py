from flask import Flask, render_template, request

# Initialization Flask
app = Flask(__name__)

# Config upload folder
app.config['UPLOAD_FOLDER'] = "static"


# Process requests
@app.route("/", methods=['POST', 'GET'])
def home():
    return "Dây là home"


# Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
