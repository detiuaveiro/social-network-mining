import data_collector
from utils import ScrapperEntity, DecisionTree, NeuralNetwork, save_classifier, open_classifier, KNeighbors, split_data
import numpy as np


def main():
    limit = None
    params = [
        ScrapperEntity('antoniocostapm', limit, "PS"),
        ScrapperEntity('psocialista', limit, "PS"),
        ScrapperEntity('tbribeiro', limit, 'PS'),
        ScrapperEntity('ebarrocomelo', limit, 'PS'),
        ScrapperEntity('aapbatista', limit, 'PS'),
        ScrapperEntity('acmendes73', limit, 'PS'),
        ScrapperEntity('FMedina_PCML', limit, 'PS'),
        ScrapperEntity('RuiRioPSD', limit, "PSD"),
        ScrapperEntity('ppdpsd', limit, "PSD"),
        ScrapperEntity('Alexandre_Poco', limit, 'PSD'),
        ScrapperEntity('anamiguel1981', limit, 'PSD'),
        ScrapperEntity('adcacunha', limit, 'PSD'),
        ScrapperEntity('malodeabreu', limit, 'PSD'),
        ScrapperEntity('catarinarf', limit, 'PSD'),
        ScrapperEntity('cludiaandr1', limit, 'PSD'),
        ScrapperEntity('cristovaonorte', limit, 'PSD'),
        ScrapperEntity('DuarteMarques', limit, 'PSD'),
        ScrapperEntity('francisco__rs', limit, 'CDS'),
        ScrapperEntity('_CDSPP', limit, 'CDS'),
        ScrapperEntity('_jalmeida_', limit, 'CDS'),
        ScrapperEntity('cristasassuncao', limit, 'CDS')
    ]

    # data_collector.init(params, n_jobs=2)

    dataPS = data_collector.merge_data_per_label("PS")
    dataPSD = data_collector.merge_data_per_label("PSD")
    dataCDS = data_collector.merge_data_per_label("CDS")

    full_data = np.concatenate((dataPS, dataPSD, dataCDS))

    print(full_data.shape)

    np.random.shuffle(full_data)

    # classifier = KNeighbors(full_data[:, 0], full_data[:, 1], 1)

    classifier = DecisionTree(full_data[:, 0], full_data[:, 1], 1000)

    # classifier = NeuralNetwork(full_data[:, 0], full_data[:, 1], alpha=0.01, Lambda=0.0, batch_size=10,
    #                            activation="logistic", iterations=1000, hidden_layer_sizes=(100, 100), verbose=True)

    classifier.train()
    save_classifier(classifier)

    for label in ["Train", "Cv", "Test"]:
        print(f"{label} set : {classifier.accuracy(label)}")

    while True:
        user_input = input(">")
        print(classifier.predict_with_input(user_input))


if __name__ == '__main__':
    main()
