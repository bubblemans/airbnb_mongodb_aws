import pymongo
import logging
import webbrowser


logging.basicConfig(level=logging.INFO)


url = 'mongodb://54.191.163.73:27017/'
myclient = pymongo.MongoClient(url)
mydb = myclient['housing']
mycol = mydb['listingAndReview']
logging.info('connected to {}'.format(url))


def case_1():
    logging.info('What are the options that have parking spots and allow people to stay more than a week?')
    docs = list(mycol.find({'$text': {'$search': 'parking'}, 'maximum_nights': {'$gte': 7}}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))


def case_2():
    logging.info('Alvin would like to release his fantastic room to the market (insert).')
    doc = {
        "id" : 123456789,
        "name" : "The best room in SF!",
        "description" : "We offer you the best room in SF. If it is not the best, free fee!",
        "host_name" : "Alvin",
        "host_location" : "San Francisco, California, United States",
        "host_neighbourhood" : "Outer Sunset",
        "host_listings_count" : 3,
        "host_total_listings_count" : 3,
        "host_verifications" : "['email', 'phone', 'reviews']",
        "host_has_profile_pic" : "t",
        "host_identity_verified" : "f",
        "neighbourhood" : "San Francisco, California, United States",
        "neighbourhood_cleansed" : "Outer Sunset",
        "latitude" : 37.7516234251,
        "longitude" : -122.4235951,
        "property_type" : "Private room in house",
        "room_type" : "Private room",
        "accommodates" : 4,
        "bathrooms_text" : "1 private bath",
        "bedrooms" : 1,
        "beds" : 2,
        "amenities" : "[\"Hangers\", \"Essentials\", \"Free street parking\", \"Coffee maker\", \"Cable TV\", \"Beach essentials\", \"Luggage dropoff allowed\", \"Extra pillows and blankets\", \"TV\", \"Refrigerator\", \"Dedicated workspace\", \"Long term stays allowed\", \"Heating\", \"Microwave\", \"Keypad\", \"Shampoo\", \"Iron\", \"Garden or backyard\", \"Hot water\", \"Wifi\", \"Lock on bedroom door\", \"Paid parking off premises\", \"First aid kit\", \"Carbon monoxide alarm\", \"Hair dryer\", \"Smoke alarm\", \"Free parking on premises\", \"Private entrance\"]",
        "price" : "$99.99"
    }
    res = mycol.insert_one(doc)
    inserted_id = res.inserted_id
    logging.info('inserted_id is {}\n'.format(inserted_id))
    return inserted_id


def case_3(inserted_id):
    logging.info('Since no one would like to book Alvin\'s room, he would like to lower the price to $77. (update)')
    mycol.update_one({"_id": inserted_id}, {"$set": { "price": "$77"}})
    res = list(mycol.find({"_id": inserted_id}))
    logging.info('Updated document: {}\n'.format(res[0]))


def case_4():
    logging.info('Alvin decides to take it down from the website. (delete)')
    res = mycol.delete_one({"_id": inserted_id})
    logging.info('{} document has been deleted\n'.format(res.deleted_count))


def case_5():
    logging.info('Bob wants to find a room that is in Cole Valley with a review score 10.')
    docs = list(mycol.find({"host_neighbourhood" : "Cole Valley", "review_scores_value" : 10}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))


def case_6():
    logging.info('Yuta wants to waste his money and rents the highest-price listing for a day in San Francisco.')
    docs = list(mycol.find().sort('price', -1).limit(1))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The desired document is:')
    logging.info('{}\n'.format(docs[0]))


def case_7():
    logging.info('Yuta wants to know the minimum price per night by the number of beds in San Francisco.')
    docs = list(mycol.aggregate([{'$group': {'_id': '$beds', 'avg_by_beds':{'$min': '$price'}}}, {'$sort': {'avg_by_beds': 1}}]))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The results are:')
    logging.info('{}\n'.format(docs))


def case_8():
    logging.info('Yuta is just curious about how many Superhosts and normal hosts there are.')
    docs = list(mycol.aggregate([{'$group': {'_id': '$host_is_superhost', 'count': {'$sum': 1}}}]))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The results are:')
    logging.info('{}\n'.format(docs))


def case_9():
    logging.info('Yuta wants to check if a host has excellent communication (host\'s communication review is more than 9.)')
    docs = list(mycol.find( { 'review_scores_communication': { '$gte': 9 } }))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))


def case_10():
    logging.info('Yuta wants to check if a house has a fine check-in procedure? (host\'s checkin review is more than 9.)')
    docs = list(mycol.find( { 'review_scores_checkin': { '$gte': 9 } }))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))


def case_11():
    logging.info('Gayle is the host and wants to increase the number of beds for a listing.')
    obj = mycol.find_one_and_update({'host_name': 'Gayle'}, {'$inc': {'beds': 2}}, {'returnNewDocument': True})
    logging.info('Returned object ID is {}.'.format(obj['_id']))


def case_12():
    logging.info('Yuta wants to know the popular neighbourhood based on the host has a good communication')
    docs = list(mycol.aggregate([
        {'$match': {'host_response_rate': '100%'}},
        {'$group': {'_id': '$neighbourhood', 'total': {'$sum': '$review_scores_rating'}}}, {'$sort': {'total': -1}}
    ]))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The results are:')
    logging.info('{}\n'.format(docs))


def case_13():
    logging.info('Gayle wants to delete his account since he needs to sell the listing.')
    docs = list(mycol.find_one_and_delete({'host_name': 'Gayle'}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The results are:')
    logging.info('{}\n'.format(docs))


def case_14():
    logging.info('Alvin wants to know his competitors - rooms in SF and has over a rating that is over 90')
    docs = list(mycol.find({ "host_location" : "San Francisco, California, United States", "review_scores_rating" : {"$gte": 93}}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))


def case_15():
    logging.info('Now, Alvin needs to take a look at the picture of his competitors - rooms in SF and has over a rating that is over 90')
    docs = list(mycol.find({ "host_location" : "San Francisco, California, United States", "review_scores_rating" : {"$gte": 93}}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))

    url = docs[0]['picture_url']
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    case_1()
    inserted_id = case_2()
    case_3(inserted_id)
    case_4()
    case_5()
    case_6()
    case_7()
    case_8()
    case_9()
    case_10()
    case_11()
    case_12()
    case_13()
    case_14()
    case_15()