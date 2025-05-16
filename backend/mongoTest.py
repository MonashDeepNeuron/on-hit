from pymongo import MongoClient 
import datetime 

#NOTE: 
# start the db: brew services start mongodb-community@8.0 
# stop the db: brew services stop mongodb-community@8.0 


# TODO: Docker to ensure everyone has the same dependencies to post data to mongodb
# TODO: Ensuring that everyone is posting to the same database so we have a central location 
# TODO: Developing the test date 

uri = 'mongodb://localhost:27017'
client = MongoClient() # might need a URI

db = client["test"] 
collection = db["posts"]

document = { 
            "name" : "Nathan", 
            "age" :  19, 
            "city" : "Melbourne", 
            } 

document_2 = { 
            "name" : "Lil Ninja", 
            "age" :  79, 
            "Dih Size": 100000000000,
            } 

result = collection.insert_one(document)
result = collection.insert_one(document_2)
print(result.inserted_id)

