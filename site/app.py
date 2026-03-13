from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

@app.route("/add_bot")
def add_bot_page():
    return "add_bot_page"