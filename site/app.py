from flask import Flask, render_template

app = Flask(__name__)

PAGES = [
    ["/", "Main"],
    ["/add_bot", "Add the bot to your server"],
    ["/commands", "Bot Commands and game rules"]
]

@app.route("/")
def index():
    return render_template("promo.html", pages=PAGES, current_page="/")

@app.route("/add_bot")
def add_bot_page():
    return render_template("add_bot.html", pages=PAGES, current_page="/add_bot")

@app.route("/commands")
def commands_page():
    return render_template("commands.html", pages=PAGES, current_page="/commands")