# airbnb_mongodb_aws
airbnb_mongodb_aws is a simple application that supports Airbnb housing management. Users can create, retrieve, update, and delete housing information. There are generally two types of users: hosts and tourists. Hosts can post their apartments for tourists to stay. It is perfect to use MongoDB for our application because the dataset in our application needs to be easy to scale, especially that there are variable data fields and different data sizes in each data entity. Moreover, we expect that there will be more read operations because users need to decide where to stay after they browse all possible options; hence, our application requires high performance data access.

# Objectives
1. Set up a cluster on AWS
2. Demonstrate end-to-end connection from application to the MongoDB cluster

# Set up and configure AWS
The specific instructions can be found [here](https://www.notion.so/A-sharded-cluster-with-replica-sets-on-AWS-EC2-1d03f21215c249ba9354710160fa6093). The cluster consists of three nodes (EC2 instance), and each node has one config server and three different shard replicas. One of the node has mongos that connect three config servers across three nodes.
And after setting up, the cluster will look like:

<img width="723" alt="Screen Shot 2021-05-07 at 5 41 04 PM" src="https://user-images.githubusercontent.com/23702266/117431089-6701fb80-af5b-11eb-91c2-1327d95f2f80.png">

# Dataset
You can retrieve the dataset using the public Airbnb data from [here](http://insideairbnb.com/get-the-data.html). We only use the most recent 45-month data in San Francisco that contains house information and reviews, and the total size is 2.21GB.
## Database
- housing
## Collection
- listingAndReview
## Index 
- id
- host_location because it is common for users to search where to stay
- (latitude, longitude, id) because we need this compound index for sharding. 
- amenities because we need to perform $text on this key


# Install
Suggest to use virtual environment or similar tools.
```bash
pip install pymongo
```

# Usage
1. Use a Python script (request.py) to scrape the most recent Airbnb housing dataset in San Francisco from this link: http://insideairbnb.com/get-the-data.html
2. Use a Python script to (preprocess.py) to merge the data in reviews.csv, like the second table in the screenshot above, into the data in listings.csv, the first table in the screenshot above. To be more specific, the listings table has an id field that exists in the reviews table, and we create a new field, reviews, inside the listings table. The new field, reviews, is an array of objects, which contains all the review information based on a listing in listings. 
3. Use a Python script (merge.py) to merge all the data across 45 months into one big json file. After merging two different kinds of csv files from 45 months, we have 2.21GB data.
4. Use a Python script (insert.py) to insert the data from the merged json file using pymongo.

```bash
python request.py
python preprocess.py
python merge.py
python insert.py
```

## Predefiend use cases
In [api.py](https://github.com/bubblemans/airbnb_mongodb_aws/blob/main/api.py), we demonstrate the ability to make CRUD queries to the MongoDB. Use case 6 - 13 are defined by Yuta Kihara.
1. What are the options that have parking spots and allow people to stay more than a week?
2. Alvin would like to release his fantastic room to the market.
3. Since no one would like to book Alvin’s room, he would like to lower the price to $77.
4. Alvin is angry that people do not appreciate his room and no one books his room, so he decides to take it down from the website
5. Bob wants to find a room that is in Cole Valley with a review score 10.
6. Yuta wants to waste his money and rents the highest-price listing for a day in San Francisco.
7. Yuta wants to know the minimum price per night by the number of beds in San Francisco.
8. Yuta is just curious about how many Superhosts and normal hosts there are.
9. Yuta wants to check if a host has excellent communication (host's communication review is more than 9.)
10. Yuta wants to check if a house has a fine check-in procedure? (host's checkin review is more than 9.)
11. Gayle is the host and wants to increase the number of beds for a listing.
12. Yuta wants to know the popular neighbourhood based on the host has a good communication
13. Gayle wants to delete his account since he needs to sell the listing.
14. Alvin wants to know his competitors - rooms in SF and and has a rating that is over 90
15. Now, Alvin needs to take a look at the picture of his competitors - rooms in SF and and has a rating that is over 90
