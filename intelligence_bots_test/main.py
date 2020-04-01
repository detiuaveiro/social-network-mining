import data_collector
from utils import ScrapperEntity, DecisionTree, NeuralNetwork, save_classifier, open_classifier, KNeighbors, split_data, \
    multi_classifier_predict
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

    """
    data_collector.init(params, n_jobs=2)

    
    dataPS = data_collector.merge_data_per_label("PS")
    dataPSD = data_collector.merge_data_per_label("PSD")
    dataCDS = data_collector.merge_data_per_label("CDS")

    full_data = np.concatenate((dataPS, dataPSD, dataCDS))

    print(full_data.shape)

    np.random.shuffle(full_data)
    

    import pickle
    with open('data.pickle', 'rb') as output:
        full_data = pickle.load(output)

    classifiers_list = []
    for i in range(1, 10):
        classifier = KNeighbors(full_data[:, 0], full_data[:, 1], i)
        classifiers_list.append(classifier)
        classifier.train()
        save_classifier(classifier, file_name=f'classifiers/KNeighbors_{i}.classifier')
    # classifier = DecisionTree(full_data[:, 0], full_data[:, 1], 1000)

    # classifier = NeuralNetwork(full_data[:, 0], full_data[:, 1], alpha=0.01, Lambda=0.0, batch_size=10,
    #                          activation="logistic", iterations=1000, hidden_layer_sizes=(50, 50), verbose=True)

    for classifier in classifiers_list:
        print(classifier.name, "->", classifier.n_neighbors)
        for label in ["Train", "Cv", "Test"]:
            print(f"{label} set : {classifier.accuracy(label)}")
    """

    classifiers_names = ["DecisionTree.classifier", "KNeighbors_7.classifier", "NeuralNetwork.classifier"]
    classifiers = [open_classifier(file_name) for file_name in classifiers_names]

    while True:
        user_input = input(">")
        print(max(multi_classifier_predict(classifiers, user_input).items(), key=lambda c: c[1])[0])


if __name__ == '__main__':
    main()
