from django.shortcuts import render
import requests
from textblob import TextBlob
from .forms import UrlForm
from django.conf import settings
from django.conf import settings


def summar_the_comments(text):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                'Authorization': f'Bearer {settings.OPEN_API_ROUTER}',
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
        summary = result['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        return f"⚠️ Error: {str(e)}"



def home(request):
    url_info = {}
    form = UrlForm(request.POST or None)
    comments_list = []
    print("API KEY:", settings.OPEN_API_ROUTER)

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