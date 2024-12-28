from textblob import TextBlob
import yfinance as yf

class SentimentAnalyzer:
    def get_sentiment(self, symbol):
        try:
            # Get news from yfinance
            stock = yf.Ticker(symbol)
            news = stock.news
            
            if not news:
                return {
                    "score": 0,
                    "sentiment": "Neutral",
                    "headlines": []
                }

            # Analyze sentiment for each headline
            headlines = []
            total_sentiment = 0
            
            for item in news[:5]:  # Analyze last 5 news items
                sentiment = TextBlob(item['title']).sentiment.polarity
                headlines.append({
                    "title": item['title'],
                    "sentiment": sentiment
                })
                total_sentiment += sentiment

            avg_sentiment = total_sentiment / len(headlines)
            sentiment_label = "Bullish" if avg_sentiment > 0.1 else "Bearish" if avg_sentiment < -0.1 else "Neutral"

            return {
                "score": round(avg_sentiment, 2),
                "sentiment": sentiment_label,
                "headlines": headlines
            }
            
        except Exception as e:
            print(f"Sentiment analysis error: {str(e)}")
            return None