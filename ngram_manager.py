from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

np.random.normal()

class NgramManager:
    INVALID_SCORE = -100

    def __init__(self, unigram_scores,
                 bigram_scores,
                 trigram_scores,
                 stop_words=None,
                 threshold=None):

        self.trigram_scores = trigram_scores
        self.bigram_scores = bigram_scores
        self.unigram_scores = unigram_scores

        self.__threshold = threshold
        self.__ignore_score = False
        self.__stop_words = stop_words

    def ignore_score(self, enabled):
        self.__ignore_score = enabled

    def find_important_unigrams(self, text: str):
        valuable_trigrams = self.find_importnat_ngrams_for_text(text,
                                                                self.unigram_scores,
                                                                (1, 1))

        return valuable_trigrams

    def find_important_bigrams(self, text: str):
        valuable_trigrams = self.find_importnat_ngrams_for_text(text,
                                                                self.bigram_scores,
                                                                (2, 2))

        return valuable_trigrams

    def find_important_trigrams(self, text: str):
        valuable_trigrams = self.find_importnat_ngrams_for_text(text,
                                                                self.trigram_scores,
                                                                (3, 3))

        return valuable_trigrams

    def find_importnat_ngrams_for_text(self, text: str, ngram_scores, ngram_range):
        ngrams = NgramManager.get_all_ngrams_for_text(text, ngram_range, self.__stop_words)

        important_ngrams = list()

        for ngram in ngrams:
            score = self.find_ngram_score(ngram_scores, ngram)
            score = round(score, 2)

            if score == self.INVALID_SCORE:
                continue

            if self.__ignore_score:
                important_ngrams.append((ngram, score))
                continue

            if self.__threshold is None:
                important_ngrams.append((ngram, score))
            else:
                if score >= self.__threshold:
                    important_ngrams.append((ngram, score))

        important_ngrams.sort(key=lambda tup: tup[1], reverse=True)

        return important_ngrams

    @staticmethod
    def find_ngram_score(ngram_scores, ngram: str):
        found_df = ngram_scores[ngram_scores['ngram'] == ngram]
        if len(found_df) == 0:
            return NgramManager.INVALID_SCORE

        return found_df['score'].values[0]

    @staticmethod
    def get_all_ngrams_for_text(text: str, ngram_range, stop_words):
        try:
            vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words=stop_words)
            countvector = vectorizer.fit_transform([text])
            ngrams = vectorizer.get_feature_names()
            return ngrams
        except Exception as e:
            print(e)
            return []