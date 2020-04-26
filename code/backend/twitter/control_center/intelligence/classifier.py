from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer
from keras import Sequential
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import layers
from sklearn.model_selection import RandomizedSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import load_model

import json
import pickle
import string
import re


def tokenize(text):
    text = re.sub(r"http\S+", "", text)
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in tokens]
    stop_words = set(stopwords.words('english'))
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


def convert_input(x_train, x_test, max_len, label, path):
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(x_train)
    vocab_size = len(tokenizer.word_index) + 1

    x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), padding='post', maxlen=max_len)
    x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), padding='post', maxlen=max_len)

    file_name = f'{label}_tokenizer.pickle'
    if path is not None:
        file_name = f'{path}/{file_name}'

    with open(file_name, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

        return x_train, x_test, vocab_size


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


def pick_best_model(x, y, label, embedding_dim=50, max_len=100, epochs=20, param_grid=None, n_jobs=-1, save_model=True,
                    model_path=None, save_logs=True, logs_path=None):
    x = [tokenize(text) for text in x]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1000, shuffle=True)

    x_train, x_test, vocab_size = convert_input(x_train, x_test, max_len, label, path=model_path)

    if param_grid is None:
        param_grid = dict(num_filters=[32, 64, 128, 256],
                          kernel_size=[3, 5, 7],
                          vocab_size=[vocab_size],
                          embedding_dim=[embedding_dim],
                          max_len=[max_len])

    model = KerasClassifier(build_fn=create_model, epochs=epochs, batch_size=10, verbose=True)

    grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, cv=4, verbose=1, n_iter=5, n_jobs=n_jobs)
    grid_result = grid.fit(x_train, y_train)

    best_model = grid_result.best_estimator_

    test_accuracy = grid.score(x_test, y_test)

    if save_model:
        model_file = f"{label}.h5"
        model_config_file = f"{label}_config.json"
        if model_path is not None:
            model_file = f"{model_path}/{model_file}"
            model_config_file = f'{model_path}/{model_config_file}'

        best_model.model.save(model_file)
        with open(model_config_file, 'w') as f:
            json.dump({
                'epochs': epochs,
                'batch_size': 10,
                'max_len': max_len,
                'padding': 'post'
            }, f)

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

    return best_model


def read_model(model_path, label):
    config_file = f'{model_path}/{label}_config.json'
    model_file = f'{model_path}/{label}.h5'
    tokenizer_file = f'{model_path}/{label}_tokenizer.pickle'

    try:
        model = load_model(model_file)

        with open(config_file, 'r') as f:
            config = json.load(f)

        with open(tokenizer_file, 'rb')  as f:
            tokenizer = pickle.load(f)
    except Exception as e:
        raise Exception(f"Error to read saved models -> {e}") from e

    return config, model, tokenizer


def predict(model_path, label, x):
    config, model, tokenizer = read_model(model_path, label)

    classifier = KerasClassifier(build_fn=create_model, epochs=config['epochs'],
                                 batch_size=config['batch_size'], verbose=True)

    classifier.model = model

    x = [tokenize(text) for text in x]

    x = pad_sequences(tokenizer.texts_to_sequences(x), padding=config['padding'], maxlen=config['max_len'])

    return model.predict(x)


def predict_soft_max(model_path, x, confidence_limit=0.7):
    with open(f'{model_path}/labels.json', 'r') as f:
        labels = json.load(f)

    best_labels = []
    for text in x:
        models = []
        for label in labels:
            confidence = predict(model_path, label, [text])
            if confidence > confidence_limit:
                models.append((confidence, label))
            else:
                models.append((0, label))
        if len(models) > 0:
            best_labels.append(sorted(models, key=lambda m: m[0], reverse=True)[0])

    return best_labels
