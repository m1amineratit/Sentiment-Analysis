from itertools import islice
from youtube_comment_downloader import *
from textblob import TextBlob

downloader = YoutubeCommentDownloader()
comments = downloader.get_comments_from_url('https://www.youtube.com/watch?v=sZ0VDpOaJgI', sort_by=SORT_BY_POPULAR)
for comment in islice(comments, 10):
    text = comment['text']
    polarity = TextBlob(text).sentiment.polarity
    
    if polarity > 0.1:
        print('\n Comment: ', comment['text'], '\n Sentiment: Negative')
    elif polarity < 0.1:
        print('\n Comment: ', comment['text'], '\n Sentiment: Positive')
    else:
        print('\n Comment: ', comment['text'], '\n Sentiment: Neutre')
