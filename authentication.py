import bcrypt
from database import users
from database import log_event


# Utility Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


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
