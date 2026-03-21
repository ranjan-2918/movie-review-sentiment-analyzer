from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob

app = Flask(__name__)

# load dataset
data = pd.read_csv("IMDB_Dataset.csv")


# Sentiment prediction using TextBlob (Thenglish version)
def predict_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.6:
        return "Vera Level 🔥", "⭐⭐⭐⭐⭐", "very_positive"

    elif polarity > 0.2:
        return "Nalla Irukku 👍", "⭐⭐⭐⭐", "positive"

    elif polarity > -0.2:
        return "Paravala 😐", "⭐⭐⭐", "neutral"

    elif polarity > -0.6:
        return "Bore-a Irukku 😕", "⭐⭐", "negative"

    else:
        return "Mokka ❌", "⭐", "very_negative"


# Genre detection
def detect_genre(text):

    text = text.lower()

    if "horror" in text:
        return "Horror 👻"

    elif "comedy" in text or "funny" in text:
        return "Comedy 😂"

    elif "action" in text or "fight" in text:
        return "Action 🔥"

    elif "love" in text or "romance" in text:
        return "Romance ❤️"

    elif "magic" in text or "fantasy" in text:
        return "Fantasy 🧙‍♂️"

    elif "crime" in text:
        return "Crime 🚔"

    else:
        return "General 🎬"


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    message = ""

    if request.method == "POST":

        movie = request.form["movie"].lower()

        count = 0

        for review in data["review"]:

            if movie in review.lower():

                short_review = " ".join(review.split()[:20])

                sentiment, stars, label = predict_sentiment(review)

                genre = detect_genre(review)

                results.append({
                    "review": short_review,
                    "sentiment": sentiment,
                    "stars": stars,
                    "genre": genre,
                    "label": label
                })

                count += 1

                if count == 3:
                    break

        if count == 0:
            message = "No reviews found for this movie 😔"

    return render_template("index.html",
                           results=results,
                           message=message)


if __name__ == "__main__":
    app.run(debug=True)