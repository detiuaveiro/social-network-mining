import data_collector
from utils import ScrapperEntity, DecisionTree
import numpy as np


def main():
    params = [
        ScrapperEntity('antoniocostapm', 10000, "PS"),
        ScrapperEntity('psocialista', 10000, "PS"),
        ScrapperEntity('RuiRioPSD', 10000, "PSD"),
        ScrapperEntity('ppdpsd', 10000, "PSD"),
        ScrapperEntity('francisco__rs', 10000, 'CDS'),
        ScrapperEntity('_CDSPP', 10000, 'CDS')
    ]

    data_collector.init(params, n_jobs=2)

    dataPS = data_collector.merge_data_per_label("PS")
    dataPSD = data_collector.merge_data_per_label("PSD")
    dataCDS = data_collector.merge_data_per_label("CDS")[:3800]

    full_data = np.concatenate((dataPS, dataPSD, dataCDS))

    np.random.shuffle(full_data)

    classifier = DecisionTree(full_data[:, 0], full_data[:, 1], 1000)

    classifier.train()

    for label in ["Train", "Cv", "Test"]:
        print(f"{label} set : {classifier.accuracy(label)}")

    while True:
        user_input = input(">")
        print(classifier.predict_with_input(user_input))


if __name__ == '__main__':
    main()
