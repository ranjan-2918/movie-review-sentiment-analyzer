import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from flask import Flask, render_template, request, jsonify
import pandas as pd

from graph_analysis import generate_movie_graph
from sentiment_model import predict_sentiment, accuracy

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ================= NLP SETUP =================

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):

    if not isinstance(text, str):
        return ""

    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)


app = Flask(__name__)


# ================= LOAD DATASETS =================

try:
    imdb_data = pd.read_csv("movie_dataset/IMDB_Dataset.csv")
    print("IMDB dataset loaded ✅")
except:
    imdb_data = None
    print("IMDB dataset not loaded ❌")


try:
    rt_movies = pd.read_csv("movie_dataset/rotten_tomatoes_movies.csv")
    print("Movies dataset loaded ✅")
except:
    rt_movies = None
    print("Movies dataset not loaded ❌")


try:
    rt_reviews = pd.read_csv("movie_dataset/rotten_tomatoes_critic_reviews.csv")
    print("Reviews dataset loaded ✅")
except:
    rt_reviews = None
    print("Reviews dataset not loaded ❌")


# ================= AUTOCOMPLETE MOVIE TITLES =================

movie_titles = []

if rt_movies is not None:
    movie_titles = rt_movies["movie_title"].dropna().str.lower().tolist()


# ================= GENRE DETECTION =================

def detect_genre(text):

    text = str(text).lower()

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


# ================= MAIN ROUTE =================

@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    message = ""

    if request.method == "POST":

        movie = request.form.get("movie", "").strip().lower()

        if movie == "":
            message = "Please enter a movie name ⚠️"

        elif rt_movies is not None and rt_reviews is not None:

            matched_movies = rt_movies[
                rt_movies["movie_title"].str.lower().str.contains(movie, na=False)
            ]

            if matched_movies.empty:

                message = "Movie not found 😔"

            else:

                movie_links = matched_movies["rotten_tomatoes_link"]

                filtered_reviews = rt_reviews[
                    rt_reviews["rotten_tomatoes_link"].isin(movie_links)
                ]

                if filtered_reviews.empty:

                    message = "No reviews found 😔"

                else:

                    for review in filtered_reviews["review_content"].dropna().head(5):

                        review = str(review)

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

                    generate_movie_graph(results)


    return render_template(
        "index.html",
        results=results,
        accuracy=accuracy,
        message=message
    )


# ================= AUTOCOMPLETE ROUTE =================

@app.route("/suggest", methods=["GET"])
def suggest():

    query = request.args.get("q", "").lower()

    if query == "":
        return jsonify([])

    suggestions = [
        title for title in movie_titles
        if query in title
    ][:8]

    return jsonify(suggestions)


# ================= RUN SERVER =================

if __name__ == "__main__":
    app.run(debug=True)