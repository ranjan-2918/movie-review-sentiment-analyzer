import pandas as pd
import nltk

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Download required NLTK data
nltk.download("stopwords")

# ================= LOAD DATASET =================

data = pd.read_csv("movie_dataset/IMDB_Dataset.csv")

# Convert labels to numeric
label_encoder = LabelEncoder()
data["sentiment_encoded"] = label_encoder.fit_transform(data["sentiment"])

# ================= TRAIN TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    data["review"],
    data["sentiment_encoded"],
    test_size=0.2,
    random_state=42
)

# ================= TF-IDF VECTORIZER =================

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=20000,
    ngram_range=(1, 2)   # improves accuracy
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ================= TRAIN MODEL =================

model = LogisticRegression(max_iter=300)
model.fit(X_train_vec, y_train)

# ================= MODEL ACCURACY =================

predictions = model.predict(X_test_vec)
accuracy = round(accuracy_score(y_test, predictions), 4)

print("Classifier Accuracy:", accuracy)


# ================= SENTIMENT MAPPING FUNCTION =================

def convert_to_5_levels(probability):

    if probability > 0.85:
        return "Vera Level 🔥", "⭐⭐⭐⭐⭐", "very_positive"

    elif probability > 0.65:
        return "Nalla Irukku 👍", "⭐⭐⭐⭐", "positive"

    elif probability > 0.45:
        return "Paravala 😐", "⭐⭐⭐", "neutral"

    elif probability > 0.25:
        return "Bore-a Irukku 😕", "⭐⭐", "negative"

    else:
        return "Mokka ❌", "⭐", "very_negative"


# ================= PREDICTION FUNCTION =================

def predict_sentiment(text):

    text_vec = vectorizer.transform([text])

    probability = model.predict_proba(text_vec)[0][1]

    sentiment, stars, label = convert_to_5_levels(probability)

    return sentiment, stars, label