from multiprocessing import Queue, Pool
import pandas as pd
from os import listdir
import numpy as np
from utils import tokenize


def merge_data_per_label(label, tweets_folder='tweets'):
    path = f'{tweets_folder}/{label}'

    label_files = [f for f in listdir(path)]

    full_data = []

    for file_name in label_files:
        data = convert_raw_data(f"{path}/{file_name}")
        converted_data = []
        for tweet in data:
            converted_data.append(tokenize(tweet))

        full_data.extend(np.array(converted_data))

    full_data = np.unique(np.array(full_data)).reshape(-1, 1)
    label_np = np.full(full_data.shape, label)

    full_data = np.append(full_data, label_np, axis=1)

    return full_data


def convert_raw_data(path_file):
    return np.unique(pd.read_csv(path_file, header=None, skiprows=1).values)


def init(entities, n_jobs=2):
    pool = Pool(processes=n_jobs)
    current_workers = []

    tasks_queue = Queue()
    for entity in entities:
        tasks_queue.put(entity)

    while True:
        if tasks_queue.empty() and current_workers == []:
            break

        if any([w.ready() for w in current_workers]) or len(current_workers) < n_jobs:
            current_workers = [c for c in current_workers if not c.ready()]
            if not tasks_queue.empty():
                task = tasks_queue.get()
                print(task)
                current_workers.append(pool.apply_async(task.get_tweets))
