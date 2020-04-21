## @package twitter.control_center
# coding: UTF-8

import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class TweetCategorizer:
	"""
	Class dedicated to categorize tweets it receives
	"""

	def __init__(self, training_data):
		"""
		Constructor that needs the initial training data to start categorizing

		@param training_data: a dictionary containing keys (the categories) to list of documents with the training data
		"""
		# Category list that will be used to categorize a tweet
		self.category_list = []

		self.ps = PorterStemmer()
		self.stemmed_data = []
		self.kmeans = None
		self.tv = TfidfVectorizer()

		# Functions to get the data and start training
		self.add_to_sd(training_data)
		self.train()

	def add_to_sd(self, data):
		"""
		Function that takes in a dictionary of data to add to its stemmed data, which will be used for the training

		@param data: dictionary that maps categories to a list of documents
		"""
		for category in data:
			for doc in data[category]:
				dataset = pd.read_csv(doc)
				for line_index in range(len(dataset)):
					stemmed_array = dataset['tweets'][line_index].split()
					stemmed = [self.ps.stem(word) for word in stemmed_array if
					           word not in set(stopwords.words('portuguese'))]
					stemmed = ' '.join(stemmed)
					self.stemmed_data.append(stemmed)
			self.category_list.append(category)

	def train(self):
		"""
		Training function that creates the k cluster of tweets
		"""
		X = self.tv.fit_transform(self.stemmed_data)
		self.kmeans = KMeans(n_clusters=len(self.category_list))
		print(X.shape)
		self.kmeans.fit(X)

	def predict(self, tweet):
		"""
		Prediction Function

		@param tweet: tweet text to be categorized
		@returns label: label string of the most likely, but if the most likely is too farfetched, it just returns Unknown
		"""
		Y = self.tv.transform([tweet])
		min_eucli_distance = min([np.linalg.norm(cluster - Y) for cluster in self.kmeans.cluster_centers_])

		label = self.kmeans.predict(Y)[0]

		print(min_eucli_distance)
		print(self.category_list[label])

		return self.category_list[label] if min_eucli_distance < 0.8 else "Unknown"


if __name__ == "__main__":
	"""
	Simple test
	"""

	path = "data/"
	tc = TweetCategorizer({
		"PS": [path + "PS/antoniocostapm_tweets.csv", path + "PS/psocialista_tweets.csv"],
		"PSD": [path + "PSD/ppdpsd_tweets.csv", path + "PSD/RuiRioPSD_tweets.csv"]
	})
	label = tc.predict("O primeiro-ministro, @antoniocostapm, \
anunciou que o Governo deu parecer favorável à proposta de \
decreto do Presidente da República para a renovação do estado de emergência por mais 15 dias.")
	print(label)
