from flask import *

from main import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('inputMain.html')


@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        userQuery = request.form['userQuery']
        print(userQuery)
        # creating object of TwitterClient Class
        api = TwitterClient()
        # calling function to get tweets
        tweets = api.get_tweets(userQuery)
        set_html(tweets)
        return redirect(f'result/{userQuery}')

    else:
        return render_template('inputMain.html')


@app.route('/result/<userQuery>')
def result(userQuery):
    return render_template("copyindex.html")


if (__name__ == "__main__"):
    app.run(debug=True)
