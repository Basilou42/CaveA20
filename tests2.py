import unittest
from classes import User, Cave, Etagere, Bouteille

class TestClasses(unittest.TestCase):

    def test_user_creation(self):
        user = User("testuser", "password123")
        self.assertEqual(user.username, "testuser")
        self.assertNotEqual(user.password_hash, "password123")  # Ensure password is hashed

    def test_password_hashing(self):
        user1 = User("user1", "password")
        user2 = User("user2", "password")
        user3 = User("user3", "differentpassword")
        self.assertEqual(user1.password_hash, user2.password_hash)  # Same password, same hash
        self.assertNotEqual(user1.password_hash, user3.password_hash)  # Different passwords, different hashes

    def test_password_verification(self):
        user = User("testuser", "password123")
        self.assertTrue(user.verify_password("password123"))
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_adding_cave(self):
        user = User("testuser", "password123")
        user.ajouter_cave("My Cave")
        self.assertEqual(len(user.caves), 1)
        self.assertEqual(user.caves[0].name, "My Cave")

    def test_listing_bottles(self):
        user = User("testuser", "password123")
        cave = Cave("Wine Cellar")
        cave.ajouter_etagere(5)
        user.ajouter_cave(cave.name)
        self.assertEqual(user.liste_bouteilles(), [])  # No bottles yet

    def test_sorting_bottles(self):
        bottle1 = Bouteille("Domaine A", "Wine A", "Red", "Region A", 2020, 20.0, "photo_a.jpg")
        bottle2 = Bouteille("Domaine B", "Wine B", "White", "Region B", 2018, 25.0, "photo_b.jpg")
        bottle3 = Bouteille("Domaine C", "Wine C", "Rose", "Region C", 2019, 15.0, "photo_c.jpg")
        user = User("testuser", "password123")
        user.ajouter_cave("My Cave")
        user.caves[0].ajouter_etagere(10)
        self.assertEqual(len(user.caves[0].etageres), 1)
        self.assertEqual(user.caves[0].etageres[0].emplacements, 10)
        user.caves[0].ajouter_bouteille(bottle1, 1)
        user.caves[0].ajouter_bouteille(bottle2, 1)
        user.caves[0].ajouter_bouteille(bottle3, 1)
        sorted_bottles = user.tri_bouteilles("prix")
        self.assertEqual(sorted_bottles[0].prix, 15.0)
        self.assertEqual(sorted_bottles[2].prix, 25.0)

    def test_adding_shelf(self):
        cave = Cave("Test Cave")
        cave.ajouter_etagere(10)
        self.assertEqual(len(cave.etageres), 1)
        self.assertEqual(cave.etageres[0].emplacements, 10)

    def test_adding_removing_bottles(self):
        bottle = Bouteille("Domaine A", "Wine A", "Red", "Region A", 2020, 20.0, "photo_a.jpg")
        cave = Cave("Test Cave")
        cave.ajouter_etagere(1)
        cave.ajouter_bouteille(bottle, 1)
        self.assertEqual(len(cave.liste_bouteilles()), 1)
        cave.retirer_bouteille(bottle)
        self.assertEqual(len(cave.liste_bouteilles()), 0)

    def test_bottle_creation(self):
        bottle = Bouteille("Domaine A", "Wine A", "Red", "Region A", 2020, 20.0, "photo_a.jpg")
        self.assertEqual(bottle.domaine, "Domaine A")
        self.assertEqual(bottle.nom, "Wine A")
        self.assertEqual(bottle.typeVin, "Red")
        self.assertEqual(bottle.annee, 2020)
        self.assertEqual(bottle.prix, 20.0)

if __name__ == '__main__':
    unittest.main()
