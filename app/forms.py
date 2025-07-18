from django import forms


class RedditUrlForm(forms.Form):
    url = forms.URLField()

class YoutubeRedditForm(forms.Form):
    url = forms.URLField()