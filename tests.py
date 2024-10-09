import unittest
from classes import User, Cave, Etagere, Bouteille, Communaute

class TestVinApp(unittest.TestCase):

	def setUp(self):
		"""Initialisation des objets pour les tests"""
		self.user1 = User("JohnDoe", "password123")
		self.user2 = User("JaneDoe", "password456")
		self.bouteille1 = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		self.bouteille2 = Bouteille("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg")
		self.user1.ajouter_cave("Cave à vin John")
		self.cave = self.user1.caves[0]
		self.cave.ajouter_etagere(5)  # Ajouter une étagère avec 5 emplacements

	def test_creation_utilisateur(self):
		"""Test de la création des utilisateurs"""
		self.assertEqual(self.user1.username, "JohnDoe")
		self.assertEqual(self.user2.username, "JaneDoe")

	def test_verification_mot_de_passe(self):
		"""Test de la vérification du mot de passe"""
		self.assertTrue(self.user1.verify_password("password123"))
		self.assertFalse(self.user1.verify_password("wrongpassword"))

	def test_ajout_cave(self):
		"""Test de l'ajout d'une cave pour un utilisateur"""
		self.assertEqual(len(self.user1.caves), 1)
		self.assertEqual(self.user1.caves[0].name, "Cave à vin John")

	def test_ajout_etagere(self):
		"""Test de l'ajout d'une étagère dans la cave"""
		self.assertEqual(len(self.cave.etageres), 1)
		self.assertEqual(self.cave.etageres[0].num_etagere, 1)

	def test_ajout_bouteille(self):
		"""Test de l'ajout d'une bouteille dans une étagère"""
		self.cave.ajouter_bouteille(self.bouteille1, 1)
		self.assertEqual(len(self.cave.etageres[0].bouteilles), 1)
		self.assertEqual(self.cave.etageres[0].bouteilles[0].nom, "Romanée-Conti")

	def test_retrait_bouteille(self):
		"""Test du retrait d'une bouteille d'une étagère"""
		self.cave.ajouter_bouteille(self.bouteille1, 1)
		self.cave.retirer_bouteille(self.bouteille1)
		self.assertEqual(len(self.cave.etageres[0].bouteilles), 0)

	def test_ajout_lots_bouteilles(self):
		"""Test de l'ajout de plusieurs bouteilles identiques en lot"""
		bouteille_lot = Bouteille("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg", quantite=10)
		self.cave.ajouter_bouteille(bouteille_lot, 1)
		self.assertEqual(self.cave.etageres[0].bouteilles[0].quantite, 10)

	def test_lister_bouteilles(self):
		"""Test de la liste des bouteilles dans toutes les caves"""
		self.cave.ajouter_bouteille(self.bouteille1, 1)
		self.cave.ajouter_bouteille(self.bouteille2, 1)
		bouteilles = self.user1.liste_bouteilles()
		self.assertEqual(len(bouteilles), 2)

	def test_tri_bouteilles(self):
		"""Test du tri des bouteilles par année"""
		self.cave.ajouter_bouteille(self.bouteille1, 1)
		self.cave.ajouter_bouteille(self.bouteille2, 1)
		bouteilles_triees = self.user1.tri_bouteilles("annee")
		self.assertEqual(bouteilles_triees[0].annee, 2015)
		self.assertEqual(bouteilles_triees[1].annee, 2016)

	def test_ajout_note_commentaire(self):
		"""Test de l'ajout d'une note et d'un commentaire à une bouteille"""
		self.bouteille1.ajouter_note_commentaire(self.user1, 5, "Excellent vin !")
		commentaires = self.bouteille1.afficher_commentaires()
		note_moyenne = self.bouteille1.afficher_note_moyenne()

		self.assertEqual(len(commentaires), 1)
		self.assertEqual(commentaires[0][1], 5)  # Vérifie la note
		self.assertEqual(commentaires[0][2], "Excellent vin !")  # Vérifie le commentaire
		self.assertEqual(note_moyenne, 5.0)  # Vérifie la note moyenne

if __name__ == '__main__':
	unittest.main()
