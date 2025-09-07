from django.http import JsonResponse
from django.shortcuts import render
import requests
from textblob import TextBlob
from .forms import RedditUrlForm, YoutubeRedditForm
from django.conf import settings
from itertools import islice
from youtube_comment_downloader import *

OPENROUTER_API_KEY="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"

def summar_the_comments(text):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes Reddit comments in 1 or 2 sentences."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this Reddit comment:\n\n\"{text}\""
                    }
                ],
                "temperature": 0.3
            }
        )

        result = response.json()

        # Debugging line (optional, remove later)
        # print(result)

        if "choices" in result and len(result["choices"]) > 0:
            summary = result["choices"][0]["message"]["content"].strip()
            return summary
        elif "error" in result:
            return f"⚠️ API Error: {result['error'].get('message', 'Unknown error')}"
        else:
            return "⚠️ Unexpected API response format."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"



def home(request):
    url_info = {}
    form = RedditUrlForm(request.POST or None)
    comments_list = []

    pos = neu = neg = 0
    if request.method == 'POST' and form.is_valid():
            url_form = form.cleaned_data['url']
            url = f'{url_form}.json'
            headers = {"User-Agent": "MyRedditScraper/0.1"}

            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                if 'error' in data:
                    url_info['error'] = data['error']

                else:
                    post_data = data[0]["data"]["children"][0]["data"]
                    url_info['title'] = post_data.get("title", "No Title")
                    url_info['selftext'] = post_data.get("selftext", "No Content")
                    
                comments = data[1]["data"]["children"]
                
                for comment in comments:
                    if comment['kind'] == "t1":
                        text = comment['data']['body']
                        polarity = TextBlob(text).sentiment.polarity
                        if polarity < 0.1:
                            sentiment_label = '😡 Negative'
                        elif polarity > 0.1:
                            sentiment_label = '😊 Positive'
                        else:
                            sentiment_label = '😐 Neutral'

                        summar_comment = summar_the_comments(text)

                        comments_list.append({
                            'body' : comment["data"]["body"],
                            'author' : comment["data"]["author"],
                            'sentiment' : sentiment_label,
                            'score' : polarity,
                            'summar_comment' : summar_comment,
                        })

                pos = sum(1 for c in comments_list if c['score'] > 0.1)
                neu = sum(1 for c in comments_list if -0.1 <= c['score'] <= 0.1)
                neg = sum(1 for c in comments_list if c['score'] < -0.1)

            except Exception as e:
                url_info = {'error' : str(e)}
            

    return render(request, 'pages/home.html', {
        'form' : form, 
        'comments_list' : comments_list, 
        'url_info' : url_info,
        'pos' : pos,
        'neu' : neu,
        'neg' : neg        
        })


def youtube_comments(request):
    comments_list = []
    pos = neg = neu = 0
    form = YoutubeRedditForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        url = form.cleaned_data['url']
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(f'{url}', sort_by=SORT_BY_POPULAR)
        try:
            for comment in islice(comments, 10):
                text = comment['text']
                polarity = TextBlob(text).sentiment.polarity
                
                if polarity < 0.1:
                    sentiment_label = '😡 Negative'
                elif polarity > 0.1:
                    sentiment_label = '😊 Positive'
                else:
                    sentiment_label = '😐 Neutral'

                summary = summar_the_comments(text)

                comments_list = ({
                    'author' : comment['author'],
                    'body' : comment['text'],
                    'score' : polarity,
                    'summary' : summary,
                    'sentiment_label' : sentiment_label,
                })
            pos = sum(1 for c in comments_list if c['score'] > 0.1)
            neg = sum(1 for c in comments_list if c['score'] < 0.1)
            neu = sum(1 for c in comments_list if -0.1 <= c['score'] <= 0.1)

        except Exception as e:
            return JsonResponse({'error' : e})
    return render(request, 'pages/youtube.html', {'comments_list' : comments_list, 'form' : form, 'pos' : pos, 'neg' : neg, 'neu' : neu})