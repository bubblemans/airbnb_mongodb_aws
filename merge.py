import pandas as pd
import json
import os


def merge_all_json():
    dirs = os.listdir('./data')
    merged = []
    for directory in dirs:
        filepath = './data/' + directory + '/listingsAndReviews.json'
        with open(filepath) as rf:
            data = json.load(rf)
            merged += data

    with open('./data/listingsAndReviews.json', 'w') as wf:
        json.dump(merged, wf, indent=4)


if __name__ == '__main__':
    merge_all_json()
