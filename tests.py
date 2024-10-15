import mysql.connector
from classes import User, Cave, Etagere, Bouteille, Communaute, get_db_connection
import pytest

# Helper function to create users
def create_users():
    """Creates and returns two users."""
    user1 = User("JohnDoe", "password123")
    user1.save()

    user2 = User("JaneDoe", "password456")
    user2.save()

    user1 = User.get_by_username("JohnDoe")
    user2 = User.get_by_username("JaneDoe")
    return user1, user2

# Helper function to create a bottle
def create_bottle(name, appellation, couleur, region, annee, prix, photo, quantite=1):
    """Creates and returns a bottle object."""
    return Bouteille(name, appellation, couleur, region, annee, prix, photo, quantite)

@pytest.fixture(scope="function")
def setup_db():
    """Initialisation de la connexion à la base de données et nettoyage"""
    db = get_db_connection()
    cursor = db.cursor()

    # Clean the database at the start of each test to avoid duplicates
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE TABLE notes_commentaires;")
    cursor.execute("TRUNCATE TABLE bouteilles;")
    cursor.execute("TRUNCATE TABLE etageres;")
    cursor.execute("TRUNCATE TABLE caves;")
    cursor.execute("TRUNCATE TABLE users;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    db.commit()

    # Créer des utilisateurs pour les tests
    user1, user2 = create_users()

    # Créer une cave pour l'utilisateur 1
    user1.ajouter_cave("Cave à vin John")

    # Récupérer la cave créée pour ajouter des étagères
    caves = Cave.get_caves_by_user(user1.user_id)
    cave1 = caves[0]

    # Ajouter une étagère avec 5 emplacements
    etagere1 = Etagere(1, 5, cave1['cave_id'])
    etagere1.ajouter_etagere(5)

    yield db, cursor, user1, user2, cave1, etagere1

    # Cleanup after each test
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE TABLE notes_commentaires;")
    cursor.execute("TRUNCATE TABLE bouteilles;")
    cursor.execute("TRUNCATE TABLE etageres;")
    cursor.execute("TRUNCATE TABLE caves;")
    cursor.execute("TRUNCATE TABLE users;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    db.commit()

def test_creation_utilisateur(setup_db):
    """Test de la création des utilisateurs et de la récupération depuis la base de données"""
    _, _, user1, user2, _, _ = setup_db
    assert user1 is not None
    assert user2 is not None
    assert user1.username == "JohnDoe"
    assert user2.username == "JaneDoe"

def test_verification_mot_de_passe(setup_db):
    """Test de la vérification du mot de passe"""
    _, _, user1, _, _, _ = setup_db
    assert user1.verify_password("password123")
    assert not user1.verify_password("wrongpassword")

def test_ajout_cave(setup_db):
    """Test de l'ajout d'une cave pour un utilisateur"""
    _, _, user1, _, cave1, _ = setup_db
    caves = Cave.get_caves_by_user(user1.user_id)
    assert len(caves) == 1
    assert caves[0]['nom'] == "Cave à vin John"

def test_ajout_etagere(setup_db):
    """Test de l'ajout d'une étagère dans la cave"""
    _, _, _, _, cave1, _ = setup_db
    etageres = Etagere.get_etageres_by_cave(cave1['cave_id'])
    assert len(etageres) == 1
    assert etageres[0]['num_etagere'] == 1

def test_ajout_bouteille(setup_db):
    """Test de l'ajout d'une bouteille dans une étagère"""
    db, cursor, _, _, _, etagere1 = setup_db
    bouteille = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    etagere1.ajouter_bouteille(bouteille)

    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    assert len(bouteilles) == 1
    assert bouteilles[0]['nom'] == "Romanée-Conti"

def test_retrait_bouteille(setup_db):
    """Test du retrait d'une bouteille d'une étagère"""
    db, cursor, _, _, _, etagere1 = setup_db
    bouteille = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    etagere1.ajouter_bouteille(bouteille)

    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    assert len(bouteilles) == 1

    cursor.execute("DELETE FROM bouteilles WHERE nom = 'Romanée-Conti'")
    db.commit()

    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    assert len(bouteilles) == 0

def test_ajout_lots_bouteilles(setup_db):
    """Test de l'ajout de plusieurs bouteilles identiques en lot"""
    _, _, _, _, _, etagere1 = setup_db
    bouteille_lot = create_bottle("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg", quantite=10)

    with pytest.raises(Exception):
        etagere1.ajouter_bouteille(bouteille_lot)

def test_lister_bouteilles(setup_db):
    """Test de la liste des bouteilles dans toutes les caves"""
    _, _, _, _, _, etagere1 = setup_db
    bouteille1 = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    bouteille2 = create_bottle("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg")

    etagere1.ajouter_bouteille(bouteille1)
    etagere1.ajouter_bouteille(bouteille2)

    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    assert len(bouteilles) == 2

def test_tri_bouteilles(setup_db):
    """Test du tri des bouteilles par année"""
    db, cursor, _, _, _, etagere1 = setup_db
    bouteille1 = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    bouteille2 = create_bottle("Château Margaux", "Margaux", "Rouge", "Bordeaux", 2016, 1200, "photo.jpg")

    etagere1.ajouter_bouteille(bouteille1)
    etagere1.ajouter_bouteille(bouteille2)

    cursor.execute("SELECT * FROM bouteilles ORDER BY annee")
    bouteilles_triees = cursor.fetchall()

    assert bouteilles_triees[0][5] == 2015  # Année
    assert bouteilles_triees[1][5] == 2016

def test_ajout_note_commentaire(setup_db):
    """Test de l'ajout d'une note et d'un commentaire à une bouteille"""
    db, cursor, user1, _, _, etagere1 = setup_db
    bouteille = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    etagere1.ajouter_bouteille(bouteille)
    
    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    bouteille_id = bouteilles[0]['bouteille_id']
    
    Communaute.ajouter_note_commentaire(user1.user_id, bouteille_id, 5, "Excellent vin !")
    
    # Modify cursor to return a dictionary
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes_commentaires WHERE bouteille_id = %s", (bouteille_id,))
    notes_commentaires = cursor.fetchall()
    
    assert len(notes_commentaires) == 1
    assert notes_commentaires[0]['note'] == 5  # Access the 'note' field directly by name
    assert notes_commentaires[0]['commentaire'] == "Excellent vin !"  # Access 'commentaire' by name

def test_calculer_note_moyenne(setup_db):
    """Test du calcul de la note moyenne d'une bouteille"""
    db, cursor, user1, user2, _, etagere1 = setup_db
    bouteille = create_bottle("Domaine de la Romanée-Conti", "Romanée-Conti", "Rouge", "Bourgogne", 2015, 15000, "photo.jpg")
    etagere1.ajouter_bouteille(bouteille)

    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere1.etagere_id)
    bouteille_id = bouteilles[0]['bouteille_id']

    Communaute.ajouter_note_commentaire(user1.user_id, bouteille_id, 4, "Très bon vin")
    Communaute.ajouter_note_commentaire(user2.user_id, bouteille_id, 5, "Excellent vin")

    moyenne = Communaute.calculer_note_moyenne(bouteille_id)
    assert moyenne == 4.5
