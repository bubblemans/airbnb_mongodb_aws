import pymongo
import logging


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    url = 'mongodb://35.167.152.223:27017/'
    myclient = pymongo.MongoClient(url)
    mydb = myclient['housing']
    mycol = mydb['listingAndReview']
    logging.info('connected to {}'.format(url))

    logging.info('What are the options that have parking spots and allow people to stay more than a week?')
    docs = list(mycol.find({'$text': {'$search': 'parking'}, 'maximum_nights': {'$gte': 7}}))
    logging.info('Found {} documents'.format(len(docs)))
    logging.info('The first document is:')
    logging.info('{}\n'.format(docs[0]))

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

    logging.info('Since no one would like to book Alvin’s room, he would like to lower the price to $77. (update)')
    mycol.update_one({"_id": inserted_id}, {"$set": { "price": "$77"}})
    res = list(mycol.find({"_id": inserted_id}))
    logging.info('Updated document: {}\n'.format(res[0]))

    logging.info('Alvin decides to take it down from the website. (delete)')
    res = mycol.delete_one({"_id": inserted_id})
    logging.info('{} document has been deleted\n'.format(res.deleted_count))
