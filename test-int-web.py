import pytest
from flask import session
from classes import User, Cave, Etagere, Bouteille, get_db_connection
from int_web import app  # Assuming your Flask app is in a file named `app.py`

@pytest.fixture(scope='function')
def client():
    # Set up the Flask test client and database cleanup before each test
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Clean up the database
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute("TRUNCATE TABLE notes_commentaires;")
            cursor.execute("TRUNCATE TABLE bouteilles;")
            cursor.execute("TRUNCATE TABLE etageres;")
            cursor.execute("TRUNCATE TABLE caves;")
            cursor.execute("TRUNCATE TABLE users;")
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            db.commit()
        yield client

def test_full_flow(client):
    """Test the full flow: create user, login, add cave, add etagere, add bottle."""

    # 1. Register a new user
    response = client.post('/register', data={
        'username': 'JohnDoe',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirect after successful registration

    # 2. Login the user
    response = client.post('/login', data={
        'username': 'JohnDoe',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirect after successful login
    with client.session_transaction() as sess:
        assert sess['user_id'] is not None  # Check that user_id is in session

    # 3. Add a cave for the user
    response = client.post('/add_cave', data={
        'cave_name': 'John’s Wine Cave'
    })
    assert response.status_code == 302  # Redirect after adding cave

    # Retrieve the cave from the database to confirm it was added
    with app.app_context():
        user = User.get_by_username('JohnDoe')
        caves = Cave.get_caves_by_user(user.user_id)
        assert len(caves) == 1
        cave_id = caves[0]['cave_id']
        assert caves[0]['nom'] == 'John’s Wine Cave'

    # 4. Add an etagere (shelf) to the cave
    response = client.post('/add_etagere', data={
        'cave_id': cave_id,
        'num_etagere': 1,
        'emplacements': 10  # Number of available spots in the shelf
    })
    assert response.status_code == 302  # Redirect after adding etagere

    # Retrieve the etagere from the database to confirm it was added
    with app.app_context():
        etageres = Etagere.get_etageres_by_cave(cave_id)
        assert len(etageres) == 1
        etagere_id = etageres[0]['etagere_id']
        assert etageres[0]['num_etagere'] == 1
        assert etageres[0]['emplacements'] == 10

    # 5. Add a bottle to the etagere
    response = client.post('/add_bottle', data={
        'etagere_id': etagere_id,
        'domaine': 'Domaine de la Romanée-Conti',
        'nom': 'Romanée-Conti',
        'type_vin': 'Rouge',
        'region': 'Bourgogne',
        'annee': 2015,
        'prix': 15000,
        'quantite': 1,
        'photo': 'photo.jpg'
    })
    assert response.status_code == 302  # Redirect after adding bottle

    # Retrieve the bottle from the database to confirm it was added
    with app.app_context():
        bouteilles = Bouteille.get_bouteilles_by_etagere(etagere_id)
        assert len(bouteilles) == 1
        assert bouteilles[0]['nom'] == 'Romanée-Conti'
        assert bouteilles[0]['domaine'] == 'Domaine de la Romanée-Conti'
        assert bouteilles[0]['annee'] == 2015
        assert bouteilles[0]['prix'] == 15000
        assert bouteilles[0]['quantite'] == 1
