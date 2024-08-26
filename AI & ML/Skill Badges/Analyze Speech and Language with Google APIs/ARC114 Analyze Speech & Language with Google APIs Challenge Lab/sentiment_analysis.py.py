import argparse
from google.cloud import language_v1

def analyze(movie_review_filename):
    # Instantiate a LanguageServiceClient
    client = language_v1.LanguageServiceClient()

    # Read the movie review file
    with open(movie_review_filename, 'r') as review_file:
        content = review_file.read()

    # Create a Document object with the contents of the file
    document = language_v1.Document(
        content=content,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Call the analyze_sentiment method on the client
    sentiment = client.analyze_sentiment(request={'document': document})

    # Output the sentiment analysis result
    print(f"Text: {content}")
    print(f"Sentiment score: {sentiment.document_sentiment.score}")
    print(f"Sentiment magnitude: {sentiment.document_sentiment.magnitude}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze sentiment of a movie review using Google Cloud Natural Language API."
    )
    parser.add_argument(
        "movie_review_filename",
        help="The filename of the movie review you'd like to analyze.",
    )
    args = parser.parse_args()
    analyze(args.movie_review_filename)
