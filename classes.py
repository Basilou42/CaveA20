import hashlib

class User:
	dernier_user_id = 0

	def __init__(self, username, password):
		User.dernier_user_id += 1
		self_user_id = User.dernier_user_id
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
		return [bouteille for cave in self.caves for etagere in cave.etageres for bouteille in etagere.bouteilles]

	def tri_bouteilles(self, attribut):
		# Trie les bouteilles selon un attribut
		return sorted(self.liste_bouteilles(), key=lambda b: getattr(b, attribut))



class Cave:
	def __init__(self, name):
		self.name = name
		self.etageres = [] # Liste des étageres
		self.compteur_etagere = 0  # Initialise un compteur d'étagère pour cette cave

	def ajouter_etagere(self, emplacements):
		self.compteur_etagere += 1
		etagere = Etagere(self.compteur_etagere, emplacements)
		self.etageres.append(etagere)

	def ajouter_bouteille(self, bouteille, num_etagere):
	    print(f"Numéro d'étagère recherché: {num_etagere}")
	    for etagere in self.etageres:
	        print(f"Numéro d'étagère actuel: {etagere.num_etagere}, Bouteilles: {etagere.bouteilles}")
	        if etagere.num_etagere == num_etagere and etagere.place_libre():
	            etagere.ajouter_bouteille(bouteille)
	            return
	    raise Exception("Plus d'espace disponible ou mauvais numéro d'étagère")

	def liste_bouteilles(self):
		return [bouteilles for etagere in self.etageres for bouteilles in etagere.bouteilles]

	def retirer_bouteille(self, bouteille):
		for etagere in self.etageres:
			if bouteille in etagere.bouteilles:
				etagere.retirer_bouteille(bouteille)
				return
		raise Exception("Bouteille non trouvée")

class Etagere:
	def __init__(self, num_etagere, emplacements):
		self.num_etagere = num_etagere
		self.emplacements = emplacements
		self.bouteilles = [] # Liste des bouteilles dans l'étagere

	def place_libre(self):
		return len(self.bouteilles) < self.emplacements

	def ajouter_bouteille(self, bouteille):
		if self.place_libre():
			self.bouteilles.append(bouteille)
		else:
			raise Exception("l'étagere est pleine !")

	def retirer_bouteille(self, bouteille):
		if bouteille in self.bouteilles:
			self.bouteilles.remove(bouteille)
		else:
			raise Exception("Bouteille non trouvée !")


class Bouteille:
	dernier_bouteille_id = 0

	def __init__(self, domaine, nom, typeVin, region, annee, prix, photo):
		Bouteille.dernier_bouteille_id += 1
		self.bouteille_id = Bouteille.dernier_bouteille_id
		self.domaine = domaine
		self.nom = nom
		self.typeVin = typeVin
		self.region = region
		self.annee = annee
		self.prix = prix
		self.photo = photo

	def supprimer_bouteille(self):
		del self

	def archiver(self, note, commentaire):
		#archive la bouteille
		self.note = note
		self.commentaire = commentaire