import string
import re

import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer
from keras import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.wrappers.scikit_learn import KerasClassifier
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

from follow_service.utils import read_model, get_labels


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def tokenize(text):
	text = re.sub(r"http\S+", "", text)
	tokens = word_tokenize(text)
	tokens = [w.lower() for w in tokens]
	table = str.maketrans('', '', string.punctuation)
	words = [w.translate(table) for w in tokens]
	stop_words = set(stopwords.words('portuguese'))
	stop_words.add('https')

	lemmatizer = WordNetLemmatizer()
	words = [lemmatizer.lemmatize(w, pos="v") for w in words if not w in stop_words and len(w) > 2]

	return ' '.join(words)


def convert_labels_to_binary(data, size):
	vectors = []

	for label in data:
		start = data[label]['start']
		end = data[label]['end']
		v = []
		for i in range(size):
			if start <= i < end:
				v.append(1)
			else:
				v.append(0)

		vectors.append(np.asarray(v))

	return vectors


def convert_input(x_train, x_test, max_len):
	tokenizer = Tokenizer(num_words=5000)
	tokenizer.fit_on_texts(x_train)
	vocab_size = len(tokenizer.word_index) + 1

	x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), padding='post', maxlen=max_len)
	x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), padding='post', maxlen=max_len)

	return x_train, x_test, vocab_size, tokenizer


def create_model(num_filters, kernel_size, vocab_size, embedding_dim, max_len):
	model = Sequential()
	model.add(layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
	model.add(layers.Conv1D(num_filters, kernel_size, activation='relu'))
	model.add(layers.GlobalMaxPooling1D())
	model.add(layers.Dense(10, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.compile(optimizer='adam',
				  loss='binary_crossentropy',
				  metrics=['accuracy'])
	return model


def pick_best_model(x, y, label, embedding_dim=50, max_len=100, epochs=20, param_grid=None, n_jobs=-1, save_logs=True,
					logs_path=None):
	x = [tokenize(text) for text in x]
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1000, shuffle=True)

	x_train, x_test, vocab_size, tokenizer = convert_input(x_train, x_test, max_len)

	if param_grid is None:
		param_grid = {
			"num_filters": [32, 64, 128, 256],
			"kernel_size": [3, 5, 7],
			"vocab_size": [vocab_size],
			"embedding_dim": [embedding_dim],
			"max_len": [max_len]
		}

	model = KerasClassifier(build_fn=create_model, epochs=epochs, batch_size=10, verbose=True)

	grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, cv=4, verbose=1, n_iter=5, n_jobs=n_jobs)
	grid_result = grid.fit(x_train, y_train)

	best_model = grid_result.best_estimator_

	test_accuracy = grid.score(x_test, y_test)

	config = {
		'epochs': epochs,
		'batch_size': 10,
		'max_len': max_len,
		'padding': 'post'
	}

	if save_logs:
		logs_file = f"{label}.log"
		if logs_path is not None:
			logs_file = f"{logs_path}/{logs_file}"

		with open(logs_file, 'a') as f:
			s = 'Running {} data set (full_dataset_size = {})\nBest Accuracy : ''{:.4f}\nTest Accuracy : {:.4f}\n\n'
			output_string = s.format(
				label,
				len(x),
				grid_result.best_score_,
				test_accuracy)
			f.write(output_string)

	return tokenizer, best_model, config


def predict(models, label, x):
	config, model, tokenizer = read_model(models, label)

	classifier = KerasClassifier(build_fn=create_model, epochs=config['epochs'],
								 batch_size=config['batch_size'], verbose=True)

	classifier.model = model

	x = [tokenize(text) for text in x]

	x = pad_sequences(tokenizer.texts_to_sequences(x), padding=config['padding'], maxlen=config['max_len'])
	output = model.predict(x)

	return output


def predict_soft_max(models, x, policy_label):
	labels = get_labels(models, policy_label)

	best_labels = []
	for text in x:
		classifiers = []
		for label in labels:
			confidence = predict(models, label, [text])
			if confidence > 0.7:
				classifiers.append((confidence, label))
		if len(classifiers) > 0:
			best_labels.append(sorted(classifiers, key=lambda m: m[0], reverse=True)[0])
		else:
			best_labels.append(None)

	return best_labels


def train_model():
	pass