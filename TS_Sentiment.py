from nltk.sentiment.vader import SentimentIntensityAnalyzer

def Text_Sentiment(text):
    sent_analyzer = SentimentIntensityAnalyzer()
    sent_analyzed = sent_analyzer.polarity_scores(text)

    result = {'negativity':sent_analyzed['neg'],'positivity':sent_analyzed['pos']}
    return result