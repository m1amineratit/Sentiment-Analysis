import requests
from bs4 import BeautifulSoup


url = 'https://www.reddit.com/r/law/comments/1lx85ay/.json'
headers = {"User-Agent": "MyRedditScraper/0.1"}

response = requests.get(url, headers=headers)
data = response.json()

post = data[0]["data"]['children'][0]['data']
title = post["title"]
selftext = post["selftext"]

print("Title: ", title)
print("comment:  ",selftext)

comments = data[1]["data"]["children"]

with open('comment.txt', 'w', encoding='utf-8') as File:
    for comment in comments:
        if comment['kind'] == "t1":
            body = comment["data"]["body"]
            author = comment["data"]["author"]
            File.write(f"\n Comment by {author}:\n{body}")