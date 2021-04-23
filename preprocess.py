import pandas as pd
import json
import os


def csv_to_dict(filename):
    df = pd.read_csv(filename)
    result = df.to_json(orient='records')
    parsed = json.loads(result)
    return parsed


def merge_listings_and_reviews(listings, reviews):
    for listing in listings:
        id = listing['id']
        reviews = [review for review in reviews if review['listing_id'] == id]
        listing['reviews'] = reviews
    return listings


def save_json(data, filename):
    with open(filename, 'w') as wf:
        json.dump(data, wf, indent=4)


if __name__ == '__main__':
    dirs = os.listdir('./data')
    for working_dir in dirs:
        listings = csv_to_dict('./data/{}/listings.csv'.format(working_dir))
        reviews = csv_to_dict('./data/{}/reviews.csv'.format(working_dir))
        data = merge_listings_and_reviews(listings, reviews)
        save_json(data, './data/{}/listingsAndReviews.json'.format(working_dir))
