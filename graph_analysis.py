import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


def generate_movie_graph(results):

    positive = 0
    negative = 0

    for r in results:
        if r["label"] in ["positive", "very_positive"]:
            positive += 1
        else:
            negative += 1

    labels = ["Positive", "Negative"]
    sizes = [positive, negative]

    plt.figure(figsize=(6,6))

    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=["#4CAF50", "#F44336"]
    )

    # Donut shape
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title("Sentiment Distribution for Selected Movie")

    plt.savefig("static/movie_sentiment_graph.png")
    plt.close()