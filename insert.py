import pymongo
import json


if __name__ == '__main__':
    filepath = './data/listingsAndReviews.json'
    with open(filepath) as rf:
        data = json.load(rf)

    client = pymongo.MongoClient('mongodb://35.167.152.223:27017/')
    print('connected')

    db = client['housing']
    col = db['listingAndReview']

    for i in range(0, len(data), 100):
        doc = data[i:i+100]
        print('inserted {} doc'.format(i))
        col.insert_one(doc)
