from classes import *

# Test création d'utilisateur 
user = User("john_doe", "supersecretpassword")
print(f"Username: {user.username}")
print(f"Password Hash: {user.password_hash}")

# test verifypassword
is_valid = user.verify_password("supersecretpassword")
print(f"Password is valid: {is_valid}")

bottle = Bouteille("Domaine A", "Wine A", "Red", "Region A", 2020, 20.0, "photo_a.jpg")
bottle1 = Bouteille("Domaine A", "Wine A", "Red", "Region A", 2010, 20.0, "photo_a.jpg")

#cave = Cave("Test Cave")
user.ajouter_cave("macave")
cave = user.caves[0]
cave.ajouter_etagere(5)
print("emplacements")
print(cave.etageres[0].emplacements)
cave.ajouter_bouteille(bottle, 1)
cave.ajouter_bouteille(bottle1, 1)
print("liste bouteilles")
print(cave.liste_bouteilles())
print("nombre de bouteilles")
print(len(cave.liste_bouteilles()))
cave.retirer_bouteille(bottle)
print(cave.liste_bouteilles())
print(len(cave.liste_bouteilles()))