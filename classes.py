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
		#print(f"Numéro d'étagère recherché: {num_etagere}")
		for etagere in self.etageres:
			#print(f"Numéro d'étagère actuel: {etagere.num_etagere}, Bouteilles: {etagere.bouteilles}")
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

	def place_libre(self, nombre_bouteilles=1):
		# Vérifie si l'étagère a assez de place pour ajouter un certain nombre de bouteilles
		return len(self.bouteilles) + nombre_bouteilles <= self.emplacements

	def ajouter_bouteille(self, bouteille):
		# On vérifie si la quantité à ajouter dépasse la capacité restante
		if self.place_libre(bouteille.quantite):
			self.bouteilles.append(bouteille)
		else:
			raise Exception("l'étagère est pleine ou pas assez de place pour ce lot de bouteilles !")

	def retirer_bouteille(self, bouteille):
		if bouteille in self.bouteilles:
			self.bouteilles.remove(bouteille)
		else:
			raise Exception("Bouteille non trouvée !")


class Bouteille:
	dernier_bouteille_id = 0

	def __init__(self, domaine, nom, typeVin, region, annee, prix, photo, quantite=1, proprietaires=None):
		Bouteille.dernier_bouteille_id += 1
		self.bouteille_id = Bouteille.dernier_bouteille_id
		self.domaine = domaine
		self.nom = nom
		self.typeVin = typeVin
		self.region = region
		self.annee = annee
		self.prix = prix
		self.photo = photo
		self.quantite = quantite
		self.proprietaires = proprietaires if proprietaires is not None else []  # Liste des utilisateurs propriétaires
		self.communaute = Communaute()  # Ajouter la communauté pour chaque bouteille

	def supprimer_bouteille(self):
		del self

	def archiver(self, note, commentaire):
		#archive la bouteille
		self.note = note
		self.commentaire = commentaire

	def ajouter_quantite(self, nombre):
		self.quantite += nombre

	def retirer_quantite(self, nombre):
		if nombre <= self.quantite:
			self.quantite -= nombre
		else:
			raise Exception("Pas assez de bouteilles en stock !")

	def ajouter_proprietaire(self, utilisateur):
		if utilisateur not in self.proprietaires:
			self.proprietaires.append(utilisateur)

	def retirer_proprietaire(self, utilisateur):
		if utilisateur in self.proprietaires:
			self.proprietaires.remove(utilisateur)

	def ajouter_note_commentaire(self, utilisateur, note, commentaire):
		self.communaute.ajouter_note_commentaire(self, utilisateur, note, commentaire)

	def afficher_note_moyenne(self):
		return self.communaute.calculer_note_moyenne(self)

	def afficher_commentaires(self):
		return self.communaute.afficher_commentaires(self)

class Communaute:
	def __init__(self):
		# Dictionnaire qui stocke les commentaires et les notes pour chaque bouteille.
		# La clé est l'ID de la bouteille, et la valeur est une liste de tuples (utilisateur, note, commentaire).
		self.notes_commentaires = {}

	def ajouter_note_commentaire(self, bouteille, utilisateur, note, commentaire):
		# Vérification de la validité de la note
		if not (0 <= note <= 5):
			raise ValueError("La note doit être entre 0 et 5.")

		# Si la bouteille n'a pas encore de notes/commentaires, initialiser la liste pour cette bouteille
		if bouteille.bouteille_id not in self.notes_commentaires:
			self.notes_commentaires[bouteille.bouteille_id] = []

		# Ajouter la note et le commentaire pour la bouteille
		self.notes_commentaires[bouteille.bouteille_id].append((utilisateur.username, note, commentaire))

	def calculer_note_moyenne(self, bouteille):
		# Vérifier si la bouteille a des notes
		if bouteille.bouteille_id not in self.notes_commentaires or len(self.notes_commentaires[bouteille.bouteille_id]) == 0:
			raise Exception("Aucune note pour cette bouteille.")

		# Calculer la moyenne des notes
		total_notes = sum(note for _, note, _ in self.notes_commentaires[bouteille.bouteille_id])
		nb_notes = len(self.notes_commentaires[bouteille.bouteille_id])
		return total_notes / nb_notes

	def afficher_commentaires(self, bouteille):
		# Vérifier si la bouteille a des commentaires
		if bouteille.bouteille_id not in self.notes_commentaires or len(self.notes_commentaires[bouteille.bouteille_id]) == 0:
			return "Aucun commentaire pour cette bouteille."

		# Afficher tous les commentaires et les notes pour la bouteille
		commentaires = self.notes_commentaires[bouteille.bouteille_id]
		return [(utilisateur, note, commentaire) for utilisateur, note, commentaire in commentaires]
