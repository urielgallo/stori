from flask import Flask
from routes.transaction_bp import transaction_bp

app = Flask(__name__)

app.register_blueprint(transaction_bp, url_prefix='/transaction')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#if __name__ == "__main__":
app.run(host='0.0.0.0', port=5050)    