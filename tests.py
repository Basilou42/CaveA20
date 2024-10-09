import unittest
import mysql.connector
from classes import User, Cave, Etagere, Bouteille, Communaute, get_db_connection

class TestVinAppDB(unittest.TestCase):

	def setUp(self):
		"""Initialisation de la connexion à la base de données et création d'utilisateurs"""
		# Connexion à la base de données
		self.db = get_db_connection()
		self.cursor = self.db.cursor()

		# Créer des utilisateurs pour les tests
		self.user1 = User("JohnDoe", "password123")
		self.user1.save()

		self.user2 = User("JaneDoe", "password456")
		self.user2.save()

		# Récupérer les utilisateurs à partir de la base de données
		self.user1 = User.get_by_username("JohnDoe")
		self.user2 = User.get_by_username("JaneDoe")

		# Créer une cave pour l'utilisateur 1
		self.user1.ajouter_cave("Cave à vin John")

		# Récupérer la cave créée pour ajouter des étagères
		caves = Cave.get_caves_by_user(self.user1.user_id)
		self.cave1 = caves[0]

		# Ajouter une étagère avec 5 emplacements
		self.etagere1 = Etagere(1, 5, self.cave1['cave_id'])
		self.etagere1.ajouter_etagere(5)


	def tearDown(self):
		"""Nettoyage de la base de données après chaque test"""
		self.cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
		self.cursor.execute("TRUNCATE TABLE notes_commentaires;")
		self.cursor.execute("TRUNCATE TABLE bouteilles;")
		self.cursor.execute("TRUNCATE TABLE etageres;")
		self.cursor.execute("TRUNCATE TABLE caves;")
		self.cursor.execute("TRUNCATE TABLE users;")
		self.cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
		self.db.commit()

	def test_creation_utilisateur(self):
		"""Test de la création des utilisateurs et de la récupération depuis la base de données"""
		self.assertIsNotNone(self.user1)
		self.assertIsNotNone(self.user2)
		self.assertEqual(self.user1.username, "JohnDoe")
		self.assertEqual(self.user2.username, "JaneDoe")

	def test_verification_mot_de_passe(self):
		"""Test de la vérification du mot de passe"""
		self.assertTrue(self.user1.verify_password("password123"))
		self.assertFalse(self.user1.verify_password("wrongpassword"))

	def test_ajout_cave(self):
		"""Test de l'ajout d'une cave pour un utilisateur"""
		caves = Cave.get_caves_by_user(self.user1.user_id)
		self.assertEqual(len(caves), 1)
		self.assertEqual(caves[0]['nom'], "Cave à vin John")

	def test_ajout_etagere(self):
		"""Test de l'ajout d'une étagère dans la cave"""
		etageres = Etagere.get_etageres_by_cave(self.cave1['cave_id'])
		self.assertEqual(len(etageres), 1)
		self.assertEqual(etageres[0]['num_etagere'], 1)

	def test_ajout_bouteille(self):
		"""Test de l'ajout d'une bouteille dans une étagère"""
		bouteille = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		self.etagere1.ajouter_bouteille(bouteille)

		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		self.assertEqual(len(bouteilles), 1)
		self.assertEqual(bouteilles[0]['nom'], "Romanée-Conti")

	def test_retrait_bouteille(self):
		"""Test du retrait d'une bouteille d'une étagère"""
		bouteille = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		self.etagere1.ajouter_bouteille(bouteille)

		# Vérifier que la bouteille a été ajoutée
		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		self.assertEqual(len(bouteilles), 1)

		# Supprimer la bouteille
		self.cursor.execute("DELETE FROM bouteilles WHERE nom = 'Romanée-Conti'")
		self.db.commit()

		# Vérifier que la bouteille a été supprimée
		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		self.assertEqual(len(bouteilles), 0)

	def test_ajout_lots_bouteilles(self):
		"""Test de l'ajout de plusieurs bouteilles identiques en lot"""
		bouteille_lot = Bouteille("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg", quantite=10)

		with self.assertRaises(Exception):
			self.etagere1.ajouter_bouteille(bouteille_lot)

	def test_lister_bouteilles(self):
		"""Test de la liste des bouteilles dans toutes les caves"""
		bouteille1 = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		bouteille2 = Bouteille("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg")

		self.etagere1.ajouter_bouteille(bouteille1)
		self.etagere1.ajouter_bouteille(bouteille2)

		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		self.assertEqual(len(bouteilles), 2)

	def test_tri_bouteilles(self):
		"""Test du tri des bouteilles par année"""
		bouteille1 = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		bouteille2 = Bouteille("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg")

		self.etagere1.ajouter_bouteille(bouteille1)
		self.etagere1.ajouter_bouteille(bouteille2)

		self.cursor.execute("SELECT * FROM bouteilles ORDER BY annee")
		bouteilles_triees = self.cursor.fetchall()

		self.assertEqual(bouteilles_triees[0][5], 2015)  # Année
		self.assertEqual(bouteilles_triees[1][5], 2016)

	def test_ajout_note_commentaire(self):
		"""Test de l'ajout d'une note et d'un commentaire à une bouteille"""
		bouteille = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		self.etagere1.ajouter_bouteille(bouteille)

		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		bouteille_id = bouteilles[0]['bouteille_id']

		Communaute.ajouter_note_commentaire(self.user1.user_id, bouteille_id, 5, "Excellent vin !")

		self.cursor.execute("SELECT * FROM notes_commentaires WHERE bouteille_id = %s", (bouteille_id,))
		notes_commentaires = self.cursor.fetchall()

		self.assertEqual(len(notes_commentaires), 1)
		self.assertEqual(notes_commentaires[0][2], 5)  # Note
		self.assertEqual(notes_commentaires[0][3], "Excellent vin !")  # Commentaire

	def test_calculer_note_moyenne(self):
		"""Test du calcul de la note moyenne d'une bouteille"""
		bouteille = Bouteille("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
		self.etagere1.ajouter_bouteille(bouteille)

		bouteilles = Bouteille.get_bouteilles_by_etagere(self.etagere1.etagere_id)
		bouteille_id = bouteilles[0]['bouteille_id']

		Communaute.ajouter_note_commentaire(self.user1.user_id, bouteille_id, 4, "Très bon vin")
		Communaute.ajouter_note_commentaire(self.user2.user_id, bouteille_id, 5, "Excellent vin")

		moyenne = Communaute.calculer_note_moyenne(bouteille_id)
		self.assertEqual(moyenne, 4.5)

if __name__ == '__main__':
	unittest.main()
