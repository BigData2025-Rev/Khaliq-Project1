from database import users
from database import orders
from database import cars
from database import log_event
from bson import ObjectId

def toContinue():
    input("Press ENTER key to continue ")

def show_users():
    print("\n--- USERS ---\n")
    for user in users.find():
        print(f"{user['name']}")
        print(f"Role: {user['role']}\n")
    toContinue()

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