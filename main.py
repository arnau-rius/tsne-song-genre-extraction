import csv
import requests
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np

numOfGenres = 5
numOfFeatures = 12


def get_dataset():
    content = []
    with open('./dataset.csv', 'r') as file:
        reader = csv.reader(file)
        [content.append(song) for song in reader]
        return content


def get_dataset_ids(dataset):
    return [song[0] for song in dataset]


def get_dataset_genres(dataset):
    genres = ['Alternative Rock', 'Classical',
              'Jazz', 'Dance & Electronic', 'Rap & Hip-Hop']
    return np.array([float(genres.index(song[1]) + 1) for song in dataset])


def get_features(dataset_ids):
    dataset_features = []
    separator = ';'
    # separate in  batches of 10 ids / request
    batch_size = 10
    num_batches = int(len(dataset_ids) / batch_size)
    dataset_ids_query_param_batches = np.array_split(dataset_ids, num_batches)
    # for each batch retreive features
    for dataset_ids_query_param_batch in dataset_ids_query_param_batches:
        dataset_ids_query_param = separator.join(dataset_ids_query_param_batch)
        url = f'https://acousticbrainz.org/api/v1/high-level?recording_ids={dataset_ids_query_param}'
        response = requests.get(url)
        response_json = response.json()
        for key in response_json:
            if(key != 'mbid_mapping'):
                data = response_json[key]['0']
                a01 = data['highlevel']['danceability']['all']['danceable']
                a02 = data['highlevel']['gender']['all']['female']
                a03 = data['highlevel']['mood_acoustic']['all']['acoustic']
                a04 = data['highlevel']['mood_aggressive']['all']['aggressive']
                a05 = data['highlevel']['mood_electronic']['all']['electronic']
                a06 = data['highlevel']['mood_happy']['all']['happy']
                a07 = data['highlevel']['mood_party']['all']['party']
                a08 = data['highlevel']['mood_relaxed']['all']['relaxed']
                a09 = data['highlevel']['mood_sad']['all']['sad']
                a10 = data['highlevel']['timbre']['all']['bright']
                a11 = data['highlevel']['tonal_atonal']['all']['tonal']
                a12 = data['highlevel']['voice_instrumental']['all']['voice']
                dataset_features.append(
                    [a01, a02, a03, a04, a05, a06, a07, a08, a09, a10, a11, a12])
    return dataset_features


def save_dataset_features(dataset_features):
    with open('dataset_features.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(dataset_features)


def get_dataset_feature():
    return np.genfromtxt('dataset_features.csv', delimiter=',')


def get_dataset_tsne(dataset_features):
    return TSNE().fit_transform(dataset_features)


def save_dataset_tsne(dataset_tsne):
    with open('dataset_tsne.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(dataset_tsne)


def save_dataset_tsne_with_genres(dataset_tsne, dataset_genres):
    dataset_tsne_with_genres = []
    for index, song_tsne in enumerate(dataset_tsne):
        dataset_tsne_with_genres.append(
            [song_tsne[0], song_tsne[1], dataset_genres[index]])
    with open('dataset_tsne_with_genres.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(dataset_tsne_with_genres)


def plot_tsne():
    x = [[] for _ in range(numOfGenres)]
    y = [[] for _ in range(numOfGenres)]
    with open('./dataset_tsne.csv', 'r') as file:
        reader = csv.reader(file)
        for song in reader:
            genre = int(float(song[2])) - 1
            x[genre].append(float(song[0]))
            y[genre].append(float(song[1]))

    plt.scatter(x[0], y[0], color='red')
    plt.scatter(x[1], y[1], color='blue')
    plt.scatter(x[2], y[2], color='green')
    plt.scatter(x[3], y[3], color='purple')
    plt.scatter(x[4], y[4], color='yellow')

    plt.show()


dataset = get_dataset()
dataset_ids = get_dataset_ids(dataset)
dataset_features = get_features(dataset_ids)
save_dataset_features(dataset_features)
dataset_features = get_dataset_feature()
dataset_tsne = get_dataset_tsne(dataset_features)
save_dataset_tsne(dataset_tsne)
dataset_genres = get_dataset_genres(dataset)
save_dataset_tsne_with_genres(dataset_tsne, dataset_genres)


def test_get_dataset_returns_list():
    dataset = get_dataset()
    assert isinstance(dataset, list)


def test_get_dataset_returns_list_of_lists():
    dataset = get_dataset()
    assert isinstance(dataset[0], list)


def test_get_dataset_ids():
    dataset = [[1, 'first row'], [2, 'second_row']]
    dataset_ids = get_dataset_ids(dataset)
    assert all([a == b for a, b in zip(
        dataset_ids, [1, 2])])
