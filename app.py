from werkzeug.wrappers import Request, Response
from flask import Flask, render_template, request

from main import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('inputMain.html')


@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        query = request.form.get("userQuery")
        print('query = ' + query)
        # creating object of TwitterClient Class
        api = TwitterClient()
        # calling function to get tweets
        tweets = api.get_tweets(query)
        set_html(tweets)
        return render_template("copyindex.html")

    else:
        return render_template('inputMain.html')


if (__name__ == "__main__"):
    from werkzeug.serving import run_simple
    app.debug = True
    run_simple('localhost', 3000, app)
