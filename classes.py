import mysql.connector
import hashlib

# Connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",   # Remplace par ton hôte MariaDB
        user="root",        # Remplace par ton utilisateur MariaDB
        password="mysqlroot",
        port=3306,# Remplace par ton mot de passe
        database="gestion_vins"
    )

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def save(self):
        db = get_db_connection()
        cursor = db.cursor()

        # Check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (self.username,))
        if cursor.fetchone()[0] > 0:
            raise Exception(f"Username '{self.username}' already exists.")
        
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                       (self.username, self.password_hash))
        db.commit()

        self.user_id = cursor.lastrowid
        cursor.close()
        db.close()


    @staticmethod
    def get_by_username(username):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()
        if user_data:
            # Create the User object without hashing the password
            user = User(user_data['username'], '')  # Pass a placeholder password
            user.password_hash = user_data['password_hash']  # Assign the password hash directly
            user.user_id = user_data['user_id']
            return user
        return None



    def ajouter_cave(self, nom):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO caves (nom, user_id) VALUES (%s, %s)", (nom, self.user_id))
        db.commit()
        cursor.close()
        db.close()

class Cave:
    def __init__(self, nom, user_id):
        self.nom = nom
        self.user_id = user_id

    @staticmethod
    def get_caves_by_user(user_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM caves WHERE user_id = %s", (user_id,))
        caves = cursor.fetchall()
        cursor.close()
        db.close()
        return caves

    def ajouter_etagere(self, emplacements):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO etageres (num_etagere, emplacements, cave_id) VALUES (%s, %s, %s)",
                       (self.num_etagere, emplacements, self.cave_id))
        db.commit()
        cursor.close()
        db.close()

class Etagere:
    def __init__(self, num_etagere, emplacements, cave_id, etagere_id=None):
        self.num_etagere = num_etagere
        self.emplacements = emplacements
        self.cave_id = cave_id
        self.etagere_id = etagere_id

    @staticmethod
    def get_etageres_by_cave(cave_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etageres WHERE cave_id = %s", (cave_id,))
        etageres = cursor.fetchall()  # Fetch all shelves associated with the given cave_id
        cursor.close()
        db.close()
        return etageres

    def ajouter_etagere(self, emplacements):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO etageres (num_etagere, emplacements, cave_id) VALUES (%s, %s, %s)",
                       (self.num_etagere, emplacements, self.cave_id))
        db.commit()
        self.etagere_id = cursor.lastrowid  # Set the etagere_id
        cursor.close()
        db.close()

    def place_libre(self, nombre_bouteilles=1):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bouteilles WHERE etagere_id = %s", (self.etagere_id,))
        nb_bouteilles = cursor.fetchone()[0]  # This should be an int if your COUNT query is correct
        cursor.close()
        db.close()

        # Ensure that self.emplacements is an integer
        if isinstance(self.emplacements, str):
            self.emplacements = int(self.emplacements)  # Convert to int if it's a string

        return nb_bouteilles + nombre_bouteilles <= self.emplacements

    def ajouter_bouteille(self, bouteille):
        db = get_db_connection()
        cursor = db.cursor()
        
        # Ensure bouteille.quantite is an integer
        if isinstance(bouteille.quantite, str):
            bouteille.quantite = int(bouteille.quantite)  # Convert to int if it's a string

        if self.place_libre(bouteille.quantite):
            cursor.execute("INSERT INTO bouteilles (domaine, nom, type_vin, region, annee, prix, photo, quantite, etagere_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (bouteille.domaine, bouteille.nom, bouteille.typeVin, bouteille.region, bouteille.annee, bouteille.prix, bouteille.photo, bouteille.quantite, self.etagere_id))
            db.commit()
        else:
            raise Exception("Pas assez de place dans l'étagère")
        
        cursor.close()
        db.close()


class Bouteille:
    def __init__(self, domaine, nom, typeVin, region, annee, prix, photo, quantite=1):
        self.domaine = domaine
        self.nom = nom
        self.typeVin = typeVin
        self.region = region
        self.annee = annee
        self.prix = prix
        self.photo = photo
        self.quantite = quantite

    @staticmethod
    def get_bouteilles_by_etagere(etagere_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bouteilles WHERE etagere_id = %s", (etagere_id,))
        bouteilles = cursor.fetchall()
        cursor.close()
        db.close()
        return bouteilles

class Communaute:
    @staticmethod
    def ajouter_note_commentaire(user_id, bouteille_id, note, commentaire):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO notes_commentaires (user_id, bouteille_id, note, commentaire) VALUES (%s, %s, %s, %s)",
                       (user_id, bouteille_id, note, commentaire))
        db.commit()
        cursor.close()
        db.close()

    @staticmethod
    def calculer_note_moyenne(bouteille_id):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT AVG(note) FROM notes_commentaires WHERE bouteille_id = %s", (bouteille_id,))
        moyenne = cursor.fetchone()[0]
        cursor.close()
        db.close()
        return moyenne
