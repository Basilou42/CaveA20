from flask import Flask, request, render_template, redirect, url_for
from classes import User, Cave, Etagere, Bouteille, Communaute

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        try:
            user.save()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and user.verify_password(password):
            return redirect(url_for('user_dashboard', username=user.username))
        else:
            return "Login failed"
    return render_template('login.html')  # Add this to handle GET requests

@app.route('/dashboard/<username>')
def user_dashboard(username):
    user = User.get_by_username(username)
    caves = Cave.get_caves_by_user(user.user_id)
    return render_template('dashboard.html', username=username, caves=caves)

@app.route('/add_cave', methods=['POST'])
def add_cave():
    username = request.form['username']
    cave_name = request.form['cave_name']
    user = User.get_by_username(username)
    user.ajouter_cave(cave_name)
    return redirect(url_for('user_dashboard', username=username))

@app.route('/cave/<cave_id>/etageres')
def show_etageres(cave_id):
    etageres = Etagere.get_etageres_by_cave(cave_id)
    return render_template('etageres.html', etageres=etageres, cave_id=cave_id)

@app.route('/etagere/<etagere_id>')
def show_etagere(etagere_id):
    # Fetch the etagere details
    etagere_data = Etagere.get_etageres_by_cave(etagere_id)[0]  # Assuming this returns a dictionary
    # Fetch the bottles in this etagere
    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere_id)
    
    return render_template('etagere.html', etagere=etagere_data, bouteilles=bouteilles)


@app.route('/add_etagere', methods=['POST'])
def add_etagere():
    cave_id = request.form.get('cave_id')  # Use .get() to safely retrieve the value
    num_etagere = request.form['num_etagere']
    emplacements = request.form['emplacements']
    print(f"Cave ID: {cave_id}, Num Etagere: {num_etagere}, Emplacements: {emplacements}")
    if cave_id:  # Check if cave_id is not empty
        # Create and add the new etagere
        etagere = Etagere(num_etagere=num_etagere, emplacements=emplacements, cave_id=cave_id)
        etagere.ajouter_etagere(emplacements)
        
        # Redirect back to the etageres page
        return redirect(url_for('show_etageres', cave_id=cave_id))
    else:
        return "Error: Cave ID is missing.", 400  # Handle missing cave_id case


@app.route('/add_bottle', methods=['POST'])
def add_bottle():
    etagere_id = request.form['etagere_id']
    domaine = request.form['domaine']
    nom = request.form['nom']
    type_vin = request.form['type_vin']
    region = request.form['region']
    annee = request.form['annee']
    prix = request.form['prix']
    quantite = request.form['quantite']
    photo = request.form['photo']

    # Retrieve the etagere by its ID, then create an Etagere instance
    etagere_data = Etagere.get_etageres_by_cave(etagere_id)[0]  # Assuming this returns a dictionary
    etagere = Etagere(etagere_data['num_etagere'], etagere_data['emplacements'], etagere_data['cave_id'], etagere_id)  # Instantiate Etagere object

    bouteille = Bouteille(domaine, nom, type_vin, region, annee, prix, photo, quantite)
    etagere.ajouter_bouteille(bouteille)  # Now this should work as etagere is an instance of Etagere

    return redirect(url_for('show_etageres', cave_id=etagere.cave_id))  # Redirect to the appropriate page

@app.route('/add_note_comment', methods=['POST'])
def add_note_comment():
    user_id = request.form['user_id']
    bouteille_id = request.form['bouteille_id']
    note = int(request.form['note'])
    commentaire = request.form['commentaire']
    Communaute.ajouter_note_commentaire(user_id, bouteille_id, note, commentaire)
    return redirect(url_for('show_etageres', cave_id=request.form['cave_id']))

if __name__ == '__main__':
    app.run(debug=True)
