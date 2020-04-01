from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from download_tweets import download_tweets
from enum import Enum, unique
from colorama import Fore, Style
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk import WordNetLemmatizer
import re
import os
from pathlib import Path
import pickle


@unique
class Status(Enum):
    SUCCESS = f"{Fore.GREEN} SUCCESS{Style.RESET_ALL}"
    ERROR = f"{Fore.RED} ERROR{Style.RESET_ALL}"
    PENDING = f"{Fore.YELLOW} PENDING{Style.RESET_ALL}"

    def __str__(self):
        return self.value


class ScrapperEntity:
    def __init__(self, username, limit, label):
        self.username = username
        self.limit = limit
        self.counter = 0
        self.tweets = []
        self.status = Status.PENDING
        self.errors = []
        self.label = label

    def get_tweets(self):

        path = f"tweets_dataset/{self.label}"
        if not os.path.exists(path):
            Path(path).mkdir(parents=True, exist_ok=True)

        file_path = f"{path}/{self.username}_tweets.csv"
        if os.path.exists(file_path):
            print(f"{Fore.BLUE} Tweets already downloaded{Style.RESET_ALL}")
            return []

        try:
            self.tweets = download_tweets(file_path=file_path,
                                          username=self.username, limit=self.limit)
            self.status = Status.SUCCESS
            self.counter = len(self.tweets)
        except Exception as e:
            self.errors.append(e)
            self.status = Status.ERROR
        print(self.__str__())
        return self.tweets

    def status_info(self):
        if self.status == Status.ERROR:
            return f"{self.status}\n\t\t-> {Fore.BLUE}{self.errors}{Style.RESET_ALL}"
        return self.status

    def __str__(self):
        return f"Username: {self.username}\n\tStatus: {self.status_info()}\n\tTweets counter: {self.counter}\n\t" \
               f"Tweets limit: {self.limit}"

    def __repr__(self):
        return self.__str__()


class Classifier:
    def __init__(self, classifier, x, y, ngram_range=(1, 2), min_df=10, max_df=1., max_features=300):
        self.classifier = classifier
        self.name = self.__class__.__name__
        self.tfidf = TfidfVectorizer(encoding='utf-8',
                                     ngram_range=ngram_range,
                                     stop_words=None,
                                     lowercase=False,
                                     max_df=max_df,
                                     min_df=min_df,
                                     max_features=max_features,
                                     norm='l2',
                                     sublinear_tf=True)
        self.x_train, self.y_train, self.x_cv, self.y_cv, self.x_test, self.y_test = self.data_initialization(x, y)

    def train(self):
        return self.classifier.fit(self.x_train, self.y_train)

    def predict(self, label='test'):
        x = eval(f'self.x_{label.lower()}')
        return self.classifier.predict(x)

    def accuracy(self, label='test'):
        y = eval(f'self.y_{label.lower()}')
        return accuracy_score(y, self.predict(label))

    def confusion_matrix(self, label='test'):
        y = eval(f'self.y_{label.lower()}')
        return confusion_matrix(y, self.predict(label))

    def data_initialization(self, x, y):
        x_train, y_train, x_cv, y_cv, x_test, y_test = split_data(x, y)
        x_train, x_cv, x_test = self.tfidf.fit_transform(x_train).toarray(), \
                                self.tfidf.transform(x_cv).toarray(), \
                                self.tfidf.transform(x_test).toarray()
        return x_train, y_train, x_cv, y_cv, x_test, y_test

    def predict_with_input(self, input_string):
        tokenized_input = np.array([tokenize(input_string)])
        return self.classifier.predict(self.tfidf.transform(tokenized_input).toarray())


class DecisionTree(Classifier):
    def __init__(self, x, y, depth=3, max_features='auto'):
        super().__init__(DecisionTreeClassifier(max_depth=depth, max_features=max_features), x, y)


class KNeighbors(Classifier):
    def __init__(self, x, y, n_neighbors, weights='distance', algorithm='auto', verbose=False):
        super().__init__(KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, algorithm=algorithm, n_jobs=-1),
                         x, y)


class NeuralNetwork(Classifier):
    def __init__(self, x, y, alpha, Lambda, hidden_layer_sizes, iterations, activation, batch_size,
                 solver="sgd", verbose=False):
        self.alpha = alpha
        self.hidden_layer_sizes = hidden_layer_sizes
        self.max_iter = iterations
        super().__init__(MLPClassifier(alpha=Lambda, learning_rate_init=alpha, activation=activation,
                                       hidden_layer_sizes=self.hidden_layer_sizes, solver=solver,
                                       max_iter=iterations, verbose=verbose, n_iter_no_change=10,
                                       batch_size=batch_size), x, y)


def split_data(x, y, train_percentage=0.6, cv_percentage=0.2):
    data_size = x.shape[0]

    train_size = int(data_size * train_percentage)
    cv_size = train_size + int(data_size * cv_percentage)

    x_train, y_train = x[:train_size], y[:train_size]
    x_cv, y_cv = x[train_size:cv_size], y[train_size:cv_size]
    x_test, y_test = x[cv_size:], y[cv_size:]

    return x_train, y_train, x_cv, y_cv, x_test, y_test


def tokenize(text):
    text = re.sub(r"http\S+", "", text)
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in tokens]
    stop_words = set(stopwords.words('english'))
    stop_words.add('https')

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w, pos="v") for w in words if not w in stop_words and len(w) > 1]

    return ' '.join(words)


def save_classifier(classifier, file_name=None, classifier_folder='classifiers'):
    Path(classifier_folder).mkdir(parents=True, exist_ok=True)
    file_path = file_name if file_name is not None else f"{classifier_folder}/{classifier.name}.classifier"
    with open(file_path, 'wb') as output:
        pickle.dump(classifier, output)


def open_classifier(file_name, classifier_folder='classifiers'):
    with open(f'{classifier_folder}/{file_name}', 'rb') as output:
        return pickle.load(output)
