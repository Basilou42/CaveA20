from classes import *

# Test création d'utilisateur 
user = User("john_doe", "supersecretpassword")
print(f"Username: {user.username}")
print(f"Password Hash: {user.password_hash}")

# test verifypassword
is_valid = user.verify_password("supersecretpassword")
print(f"Password is valid: {is_valid}")
