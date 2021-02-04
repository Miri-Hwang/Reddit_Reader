import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")
db = []

# 언어를 넣으면 db에 포스팅 내역 dict 추가


def load_posts(language):
    url = f"https://www.reddit.com/r/{language}/top/?t=month"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    posts = soup.find('div', {'class': 'rpBJOHq2PR60pnwJlUyP0'}).find_all(
        'div', {'class': 'scrollerItem'})
    for post in posts:
        votes = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).string

        try:
            votes = int(votes)
            title = post.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).string
            db.append({'title': title, 'votes': votes, 'language': language})
        except:
            pass
    print(db)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/read")
def read():
    subreddit = request.args.getlist('subreddits')

    return render_template('read.html', subreddits=subreddit)


app.run(host="127.0.0.1")
