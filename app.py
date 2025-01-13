import authentication
import admin 
import customer
from database import log_event


# # List Inventory
# def list_inventory():
#     print("\n--- Dealership Inventory ---")
#     for car in cars.find():
#         print(
#             f"ID: {car['_id']}\n"
#             f"Make: {car['make']}\n"
#             f"Model: {car['model']}\n"
#             f"Year: {car['year']}\n"
#             f"Mileage: {car['mileage']} miles\n"
#             f"Title: {car['title'].capitalize()}\n"
#             f"Previous Owners: {car['number_of_owners']}\n"
#             f"Condition: {car['condition'].capitalize()}\n"
#             f"Price: ${car['price']}\n"
#             f"Stock: {car['stock']} units\n"
#             "-----------------------------"
#         )

# # View User's Orders
# def view_my_orders(user):
#     print("\n--- Your Orders ---")
#     user_orders = orders.find({"user_id": user["_id"]})
    
#     has_orders = False
#     for order in user_orders:
#         has_orders = True
#         car = cars.find_one({"_id": ObjectId(order["car_id"])})
#         print(
#             f"Order ID: {order['_id']}\n"
#             f"Car: {car['make']} {car['model']} ({car['year']})\n"
#             f"Quantity: {order['quantity']}\n"
#             f"Order Date: {order['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
#             "-----------------------------"
#         )
    
#     if not has_orders:
#         print("You have not placed any orders yet.")
    
#     toContinue()

# # User Dashboard
# def user_dashboard(user):
#     while True:
#         print("\n--- User Dashboard ---")
#         print("1. View Available Cars")
#         print("2. Purchase Car")
#         print("3. View Owned Cars")
#         print("4. View my orders")
#         print("5. Logout")
#         choice = input("Enter your choice: ")
        
#         if choice == "1":
#             break
#         elif choice == "2":
#             purchase_car(user)
#         elif choice == "3":
#             view_owned_cars(user)
#         elif choice == "4":
#             view_my_orders(user)
#         elif choice == "5":
#             break
#         else:
#             print("Invalid choice.")


# # Purchase Car
# def purchase_car(user):
#     print("\n--- Purchase Car ---")
#     print("Available Cars:")
#     view_cars()
#     car_id = input("Enter the ID of the car you want to purchase: ")
#     quantity = int(input("Enter the quantity: "))
    
#     car = cars.find_one({"_id": ObjectId(car_id)})
#     if car and car["stock"] >= quantity:
#         cars.update_one({"_id": ObjectId(car_id)}, {"$inc": {"stock": -quantity}})
#         orders.insert_one({
#             "user_id": user["_id"],
#             "car_id": car_id,
#             "quantity": quantity,
#             "date": datetime.now()
#         })
#         users.update_one({"_id": user["_id"]}, {"$push": {"owned_cars": car}})
#         log_event(f"User {user['email']} purchased {quantity} of {car['make']} {car['model']}.")
#         print("Purchase successful!")
#     else:
#         print("Insufficient stock or invalid car ID.")

# # View Owned Cars
# def view_owned_cars(user):
#     print("\n--- Cars You Own ---")
#     user_data = users.find_one({"_id": user["_id"]})
    
#     if len(user_data['owned_cars']) == 0:
#         print("\n You do not own any cars at the moment\n")

#     for car in user_data.get("owned_cars", []):
#         print(
#             f"Make: {car['make']}\n"
#             f"Model: {car['model']}\n"
#             f"Year: {car['year']}\n"
#             f"Mileage: {car['mileage']} miles\n"
#             f"Title: {car['title'].capitalize()}\n"
#             f"Previous Owners: {car['number_of_owners']}\n"
#             f"Condition: {car['condition'].capitalize()}\n"
#             f"Price: ${car['price']}\n"
#             "-----------------------------"
#         )
#     toContinue()

# Main Menu
def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user = authentication.login()
            if user:
                if user["role"] == "admin":
                    admin.admin_dashboard()
                elif user["role"] == "privileged_user":
                    admin.admin_dashboard()
                else:
                    customer.user_dashboard(user)
        elif choice == "2":
            authentication.register()
        elif choice == "3":
            log_event("Application exited.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
