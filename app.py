import pymongo
import bcrypt
from datetime import datetime
import logging
from bson import ObjectId


# Setup Logging
logging.basicConfig(filename="store_app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# MongoDB Client Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["car_dealership"]

# Collections
users = db["users"]
cars = db["cars"]
orders = db["orders"]

# Utility Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def log_event(event):
    logging.info(event)

# User Authentication
def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user = users.find_one({"email": email})
    if user and check_password(user["password"], password):
        print(f"Welcome, {user['name']}!")
        log_event(f"User {email} logged in.")
        return user
    else:
        print("Invalid email or password.")
        return None

# User Registration
def register():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    if users.find_one({"email": email}):
        print("Email already exists.")
    else:
        hashed = hash_password(password)
        users.insert_one({"name": name, "email": email, "password": hashed, "role": "user", "owned_cars": []})
        print("Registration successful!")
        log_event(f"User {email} registered.")

def show_users():
    print("\n--- USERS ---\n")
    for user in users.find():
        print(f"{user['name']}")
        print(f"Role: {user['role']}\n")
    toContinue()

def toContinue():
    input("Press ENTER key to continue ")

# Admin Dashboard
def admin_dashboard():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View All Users")
        print("2. View All Orders")
        print("3. Modify Inventory")
        print("4. List Inventory")
        print("5. Grant Inventory Privileges")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            show_users()
        elif choice == "2":
            view_all_orders()  
        elif choice == "3":
            modify_inventory()
        elif choice == "4":
            view_cars()
        elif choice == "5":
            grant_inventory_privileges()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

# Grant Inventory Privileges
def grant_inventory_privileges():
    print("\n--- Grant Inventory Privileges ---")
    email = input("Enter the email of the user to grant privileges: ")
    user = users.find_one({"email": email})
    if user:
        if user["role"] == "privileged_user":
            print(f"User {email} already has inventory privileges.")
        else:
            users.update_one({"email": email}, {"$set": {"role": "privileged_user"}})
            log_event(f"User {email} granted inventory privileges.")
            print(f"User {email} has been granted inventory privileges.")
    else:
        print(f"No user found with email {email}.")

# Modify Inventory
def modify_inventory():
    print("\n--- Modify Inventory (Cars) ---")
    print("1. Add Car")
    print("2. Update Stock")
    print("3. Delete Car")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        make = input("Enter car make (e.g., Toyota): ")
        model = input("Enter car model (e.g., Corolla): ")
        year = int(input("Enter car year (e.g., 2020): "))
        mileage = int(input("Enter mileage (e.g., 50000): "))
        title = input("Enter title (clean or salvage): ").lower()
        number_of_owners = int(input("Enter number of previous owners: "))
        condition = input("Enter condition (excellent, good, fair): ").lower()
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        
        cars.insert_one({
            "make": make,
            "model": model,
            "year": year,
            "mileage": mileage,
            "title": title,
            "number_of_owners": number_of_owners,
            "condition": condition,
            "price": price,
            "stock": stock
        })
        log_event(f"Car {make} {model} added to inventory.")
        print("Car added to inventory.")
    
    elif choice == "2":
        car_id = input("Enter car ID: ")
        stock = int(input("Enter new stock quantity: "))
        cars.update_one({"_id": car_id}, {"$set": {"stock": stock}})
        log_event(f"Car {car_id} stock updated to {stock}.")
        print("Stock updated.")
    
    elif choice == "3":
        car_id = input("Enter car ID: ")
        try:
            car = cars.find_one({"_id": ObjectId(car_id)})
            if car:
                if car["stock"] > 1:
                    # Decrement the stock count by 1
                    cars.update_one({"_id": ObjectId(car_id)}, {"$inc": {"stock": -1}})
                    log_event(f"Stock decremented for car {car_id}. New stock: {car['stock'] - 1}.")
                    print(f"One car removed from stock. Remaining stock: {car['stock'] - 1}.")
                else:
                    # Delete the car if stock is 1
                    cars.delete_one({"_id": ObjectId(car_id)})
                    log_event(f"Car {car_id} deleted from inventory (stock was 1).")
                    print("Car deleted from inventory.")
            else:
                print("Car not found.")
        except Exception as e:
            print("Error:", e)
    
    else:
        print("Invalid choice.")

# List Inventory
def list_inventory():
    print("\n--- Dealership Inventory ---")
    for car in cars.find():
        print(
            f"ID: {car['_id']}\n"
            f"Make: {car['make']}\n"
            f"Model: {car['model']}\n"
            f"Year: {car['year']}\n"
            f"Mileage: {car['mileage']} miles\n"
            f"Title: {car['title'].capitalize()}\n"
            f"Previous Owners: {car['number_of_owners']}\n"
            f"Condition: {car['condition'].capitalize()}\n"
            f"Price: ${car['price']}\n"
            f"Stock: {car['stock']} units\n"
            "-----------------------------"
        )
# View All Orders (Admin)
def view_all_orders():
    print("\n--- All Orders ---")
    all_orders = orders.find()
    
    has_orders = False
    for order in all_orders:
        has_orders = True
        user = users.find_one({"_id": ObjectId(order["user_id"])})
        car = cars.find_one({"_id": ObjectId(order["car_id"])})
        print(
            f"Order ID: {order['_id']}\n"
            f"User: {user['name']} (Email: {user['email']})\n"
            f"Car: {car['make']} {car['model']} ({car['year']})\n"
            f"Quantity: {order['quantity']}\n"
            f"Order Date: {order['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            "-----------------------------"
        )
    
    if not has_orders:
        print("No orders have been placed yet.")
    toContinue()

# View User's Orders
def view_my_orders(user):
    print("\n--- Your Orders ---")
    user_orders = orders.find({"user_id": user["_id"]})
    
    has_orders = False
    for order in user_orders:
        has_orders = True
        car = cars.find_one({"_id": ObjectId(order["car_id"])})
        print(
            f"Order ID: {order['_id']}\n"
            f"Car: {car['make']} {car['model']} ({car['year']})\n"
            f"Quantity: {order['quantity']}\n"
            f"Order Date: {order['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            "-----------------------------"
        )
    
    if not has_orders:
        print("You have not placed any orders yet.")
    
    toContinue()

# User Dashboard
def user_dashboard(user):
    while True:
        print("\n--- User Dashboard ---")
        print("1. View Available Cars")
        print("2. Purchase Car")
        print("3. View Owned Cars")
        print("4. View my orders")
        print("5. Logout")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_cars()
        elif choice == "2":
            purchase_car(user)
        elif choice == "3":
            view_owned_cars(user)
        elif choice == "4":
            view_my_orders(user)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# View Cars
def view_cars():
    print("\n--- Available Cars ---")
    for car in cars.find({"stock": {"$gt": 0}}):
        print(
            f"ID: {car['_id']}\n"
            f"Make: {car['make']}\n"
            f"Model: {car['model']}\n"
            f"Year: {car['year']}\n"
            f"Mileage: {car['mileage']} miles\n"
            f"Title: {car['title'].capitalize()}\n"
            f"Previous Owners: {car['number_of_owners']}\n"
            f"Condition: {car['condition'].capitalize()}\n"
            f"Price: ${car['price']}\n"
            f"Stock: {car['stock']} units\n"
            "-----------------------------"
        )
    toContinue()

# Purchase Car
def purchase_car(user):
    print("\n--- Purchase Car ---")
    print("Available Cars:")
    view_cars()
    car_id = input("Enter the ID of the car you want to purchase: ")
    quantity = int(input("Enter the quantity: "))
    
    car = cars.find_one({"_id": ObjectId(car_id)})
    if car and car["stock"] >= quantity:
        cars.update_one({"_id": ObjectId(car_id)}, {"$inc": {"stock": -quantity}})
        orders.insert_one({
            "user_id": user["_id"],
            "car_id": car_id,
            "quantity": quantity,
            "date": datetime.now()
        })
        users.update_one({"_id": user["_id"]}, {"$push": {"owned_cars": car}})
        log_event(f"User {user['email']} purchased {quantity} of {car['make']} {car['model']}.")
        print("Purchase successful!")
    else:
        print("Insufficient stock or invalid car ID.")

# View Owned Cars
def view_owned_cars(user):
    print("\n--- Cars You Own ---")
    user_data = users.find_one({"_id": user["_id"]})
    
    if len(user_data['owned_cars']) == 0:
        print("\n You do not own any cars at the moment\n")

    for car in user_data.get("owned_cars", []):
        print(
            f"Make: {car['make']}\n"
            f"Model: {car['model']}\n"
            f"Year: {car['year']}\n"
            f"Mileage: {car['mileage']} miles\n"
            f"Title: {car['title'].capitalize()}\n"
            f"Previous Owners: {car['number_of_owners']}\n"
            f"Condition: {car['condition'].capitalize()}\n"
            f"Price: ${car['price']}\n"
            "-----------------------------"
        )
    toContinue()

# Main Menu
def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user = login()
            if user:
                if user["role"] == "admin":
                    admin_dashboard()
                elif user["role"] == "privileged_user":
                    admin_dashboard()
                else:
                    user_dashboard(user)
        elif choice == "2":
            register()
        elif choice == "3":
            log_event("Application exited.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
