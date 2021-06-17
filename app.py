from flask import *
from main import *


def set_html(tweets):

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # picking neutral tweets from tweets
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    textTweet = []
    cleanTweet = []
    sentimentTweet = []
    for i in range(0, len(tweets)):
        textTweet.append(tweets[i]['text'])
    for i in range(0, len(tweets)):
        cleanTweet.append(tweets[i]['clean tweet'])
    for i in range(0, len(tweets)):
        sentimentTweet.append(tweets[i]['sentiment'])

    # Create a dataframe of collected tweets
    df = pd.concat([
        pd.DataFrame(textTweet, columns=['tweet']),
        pd.DataFrame(cleanTweet, columns=['cleantweet'])
    ],axis=1)
    df = pd.concat([df, pd.DataFrame(sentimentTweet, columns=['sentiment'])], axis=1)

    wcloud = ' '.join([i for i in df['cleantweet']])

    wordcloud = WordCloud(width=1000,
                          height=700,
                          random_state=21,
                          max_font_size=120).generate(wcloud)
    dir_path = os.path.dirname(__file__)

    for fname in os.listdir(dir_path + '/static/css/images'):
      if fname.startswith('img_'):
        os.remove(dir_path + "/static/css/images/" + fname)

    image_name = "img_{}.png".format(str(uuid.uuid4()))
    wordcloud.to_file('static/css/images/{}'.format(image_name))
    
    return ptweets,ntweets,neutweets,image_name


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
        ptweets, ntweets, neutweets, image_name = set_html(tweets)
        return render_template('index.html', pos_tweets=ptweets, neg_tweets=ntweets, neutral_tweets=neutweets, img_name=image_name)

    else:
        return render_template('inputMain.html')


if (__name__ == "__main__"):
    app.run(debug=True)
