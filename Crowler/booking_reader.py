import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils import Utils


class BookingReader:

    def __init__(self):
        pass


    @staticmethod
    def read_reviews_from_urls(urls):
        frames = []
        for url in urls:
            df = BookingReader.parse_reviews_from_url(url)
            frames.append(df)

        return pd.concat(frames)

    @staticmethod
    def parse_reviews_from_url(url):
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        reviews = soup.findAll("li", class_="review_item")

        ratingValues, maxRatingValues, titles, pos_texts, neg_texts = [], [], [], [], []
        for review in reviews:
            review_soup = BeautifulSoup(str(review), 'html.parser')
            try:
                ratingValue, bestRating = BookingReader.parse_rating(review_soup)
                title = BookingReader.parse_title(review_soup)
                pos_text, neg_text = BookingReader.pase_pos_and_neg(review_soup)

                ratingValues.append(ratingValue)
                maxRatingValues.append(bestRating)
                titles.append(title)

                pos_texts.append(pos_text)
                neg_texts.append(neg_text)

            except Exception as error:
                print(error)
                print(url)
                print("####################################")
                continue

        return pd.DataFrame({'title': titles,
                             'pos_text': pos_texts,
                             'neg_text': neg_texts,
                             'ratingValue': ratingValues,
                             'bestRating': maxRatingValues})


    @staticmethod
    def parse_title(review_soup):
        title = review_soup.find('div', class_='review_item_header_content').text
        title = title.strip()[1:-1]

        return BookingReader.preprocess_text(title)

    @staticmethod
    def parse_rating(review_soup):
        value = review_soup.find('span', itemprop='reviewRating').find('meta', itemprop="ratingValue").get('content')
        maxValue = review_soup.find('span', itemprop='reviewRating').find('meta', itemprop="bestRating").get('content')

        return float(value), float(maxValue)

    @staticmethod
    def pase_pos_and_neg(review_soup):
        pos_text, neg_text = None, None

        review_pos = review_soup.find('p', class_='review_pos')
        if review_pos is not None:
            pos_text = review_pos.text.strip()
            pos_text = BookingReader.preprocess_text(pos_text)

        review_neg = review_soup.find('p', class_='review_neg')
        if review_neg is not None:
            neg_text = review_neg.text.strip()
            neg_text = BookingReader.preprocess_text(neg_text)

        if pos_text is None:
            pos_text = ""

        if neg_text is None:
            neg_text = ""

        return pos_text, neg_text

    @staticmethod
    def preprocess_text(text):
        if '\r' in text:
            return text.replace('\r', ' ')
        return text


if __name__ == "__main__":
    filepath = "../data/links/odesa-hotel-reviews.txt"

    urls = Utils.read_links(filepath)

    df = BookingReader.read_reviews_from_urls(urls)

    a = 10





