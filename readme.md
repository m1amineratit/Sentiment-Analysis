# 🔍 Reddit Sentiment & Summary Analyzer

Analyze Reddit post comments using NLP and LLMs. Get detailed sentiment scores and summaries — fast and accurate.

---

## 📦 Features

* ✅ Reddit post + comment scraper using `praw`
* 🧠 Comment-level sentiment analysis with `TextBlob`
* 🤖 LLM summarization using `OpenRouter` (e.g. Mistral 7B)
* 📊 Global sentiment score: positive / neutral / negative
* 🦾 Summary of entire comment thread

---

## ⚙️ Tech Stack

| Layer    | Tech                               |
| -------- | ---------------------------------- |
| Backend  | Django, Python                     |
| Scraping | Requests                           |
| NLP      | TextBlob                           |
| LLM API  | OpenRouter.ai (`mistral-7b`, etc.) |
| Frontend | HTML, CSS                          |

---

## 🚀 Getting Started

```bash
# Clone the Repository
mkdir sentiment_web
cd sentiment_web
git clone https://github.com/m1amineratit/Sentiment-Analysis.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all required Python packages
cd Sentiment-Analysis
pip install -r requirements.txt

# Create .env file and add your keys
echo "REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_user_agent
OPEN_API_ROUTER=your_openrouter_api_key" > .env

# Run Django server
python manage.py runserver
```

---

## 🌎 Live Demo / UI Preview

Coming soon...

---

## 🛠️ Configuration Notes

* Make sure your Reddit API credentials are valid. You can generate them [here](https://www.reddit.com/prefs/apps).
* The OpenRouter API requires an API key; register and get one from [https://openrouter.ai/](https://openrouter.ai/)
* LLMs like Mistral 7B or DeepSeek can be used to generate summaries efficiently.

---

## 💪 Contribute

Found a bug or have an idea to improve the project? PRs welcome!

---

## 🚀 Project Idea

Many people use Reddit to post about their projects and get feedback. But often the feedback is vague, hard to interpret, or scattered. That's why this tool was built — it automatically analyzes your Reddit post and comments, summarizes them, performs sentiment analysis, and gives a general ranking and clarity overview for each one.
