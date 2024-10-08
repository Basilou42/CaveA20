import hashlib

class User:
	def __init__(self, username, password):
		self.username = username
		self.password_hash = self.hash_password(password)
		self.caves = []  # List des caves appartenant a l'utilisateur

	def hash_password(self, password):
		#Crée un hash SHA-256 du mot de passe utilisateur
		return hashlib.sha256(password.encode()).hexdigest()

	def verify_password(self, password):
		#Verifie si le mot de passe entré correspond au hash du mot de passe
		return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

	def ajouter_cave(self, nom):
		# crée une nouvelle cave pour l'utilisateur
		new_cave = Cave(nom)
		self.caves.append(new_cave)

	def liste_bouteilles(self):
		# renvoie une liste de toutes les bouteilles dans toutes les caves possédées par l'utilisateur
		return [bouteile for cave in self.caves for bouteilles in cave.liste_bouteilles()]

	def tri_bouteilles(self, attribut):
		# Trie les bouteilles selon un attribut
		return sorted(self.liste_bouteilles(), key=lambda b: getattr(b, attribute))
