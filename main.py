import csv
import requests


def get_dataset():
    content = []
    with open('./dataset.csv', 'r') as file:
        reader = csv.reader(file)
        [content.append(song) for song in reader]
        return content


def get_dataset_ids(dataset):
    return [song[0] for song in dataset]


def get_features(dataset_ids):
    dataset_features = []
    separator = ';'
    dataset_ids_query_param = separator.join(dataset_ids[:10])
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
                [key, a01, a02, a03, a04, a05, a06, a07, a08, a09, a10, a11, a12])
    return dataset_features


def save_dataset_features(dataset_features):
    with open('dataset_features.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(dataset_features)


dataset = get_dataset()
dataset_ids = get_dataset_ids(dataset)
dataset_features = get_features(dataset_ids)
save_dataset_features(dataset_features)
// TODO: compute tsne using bhtsne lib


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
