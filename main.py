import pandas as pd

# load dataset
data = pd.read_csv("IMDB_Dataset.csv")

print("Dataset Loaded Successfully")
print("Total Reviews:", len(data))


# sentiment + rating prediction
def predict_sentiment_and_rating(text):

    positive_words = ["good","great","excellent","amazing","awesome","fantastic","best","love"]
    negative_words = ["bad","worst","boring","terrible","awful","hate","waste"]

    words = text.lower().split()

    score = 0

    for word in words:
        if word in positive_words:
            score += 1
        if word in negative_words:
            score -= 1

    # sentiment type
    if score >= 3:
        sentiment = "Very Positive"
        rating = "5 ⭐"
    elif score == 2:
        sentiment = "Positive"
        rating = "4 ⭐"
    elif score == 1:
        sentiment = "Slightly Positive"
        rating = "3 ⭐"
    elif score == 0:
        sentiment = "Neutral"
        rating = "3 ⭐"
    elif score == -1:
        sentiment = "Negative"
        rating = "2 ⭐"
    else:
        sentiment = "Very Negative"
        rating = "1 ⭐"

    return sentiment, rating


# genre detection
def detect_genre(text):

    horror_words = ["horror","ghost","monster","scary","fear","blood"]
    comedy_words = ["funny","comedy","laugh","hilarious","joke"]
    action_words = ["fight","battle","action","explosion","war"]
    romance_words = ["love","romance","relationship","couple","kiss"]
    fantasy_words = ["magic","dragon","fantasy","kingdom","wizard"]

    text = text.lower()

    if any(word in text for word in horror_words):
        return "Horror"
    elif any(word in text for word in comedy_words):
        return "Comedy"
    elif any(word in text for word in action_words):
        return "Action"
    elif any(word in text for word in romance_words):
        return "Romance"
    elif any(word in text for word in fantasy_words):
        return "Fantasy"
    else:
        return "General Movie"


# ask movie name
movie_name = input("\nEnter Movie Name: ").lower()

print("\nReviews Related to:", movie_name)
print("------------------------------------")

count = 0

for review in data["review"]:

    if movie_name in review.lower():

        sentiment, rating = predict_sentiment_and_rating(review)
        genre = detect_genre(review)

        print("\nReview:", review[:200])
        print("Sentiment:", sentiment)
        print("Rating:", rating)
        print("Movie Type:", genre)
        print("------------------------------------")

        count += 1

        if count == 5:
            break


if count == 0:
    print("No reviews found for this movie name.")