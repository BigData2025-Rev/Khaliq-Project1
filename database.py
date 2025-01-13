import pymongo
import logging



# MongoDB Client Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["car_dealership"]

# Collections
users = db["users"]
cars = db["cars"]
orders = db["orders"]

# Setup Logging
logging.basicConfig(filename="store_app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(event):
    logging.info(event)