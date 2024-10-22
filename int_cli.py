import argparse
from classes import User, Cave, Etagere, Bouteille  # Assuming you import from the existing code

def add_cave(user_id, nom):
    user = User.get_by_user_id(user_id)
    if user:
        user.ajouter_cave(nom)
        print(f"Cave '{nom}' added for user ID {user_id}.")
    else:
        print(f"User with ID {user_id} not found.")

def delete_cave(cave_id):
    Cave.delete_cave(cave_id)
    print(f"Cave with ID {cave_id} deleted.")

def add_etagere(cave_id, num_etagere, emplacements):
    cave = Cave.get_caves_by_user(cave_id)
    if cave:
        etagere = Etagere(num_etagere, emplacements, cave_id)
        etagere.ajouter_etagere(emplacements)
        print(f"Etagere {num_etagere} added to cave ID {cave_id}.")
    else:
        print(f"Cave with ID {cave_id} not found.")

def delete_etagere(etagere_id):
    Etagere.delete_etagere(etagere_id)
    print(f"Etagere with ID {etagere_id} deleted.")

def add_bottle(etagere_id, domaine, nom, typeVin, region, annee, prix, photo, quantite):
    etagere = Etagere.get_etagere_by_id(etagere_id)
    if etagere:
        bouteille = Bouteille(domaine, nom, typeVin, region, annee, prix, photo, quantite)
        etagere.ajouter_bouteille(bouteille)
        print(f"Bottle '{nom}' added to etagere ID {etagere_id}.")
    else:
        print(f"Etagere with ID {etagere_id} not found.")

def delete_bottle(bouteille_id):
    Bouteille.delete_bottle(bouteille_id)
    print(f"Bottle with ID {bouteille_id} deleted.")

def list_caves(user_id):
    caves = Cave.get_caves_by_user(user_id)
    for cave in caves:
        print(f"Cave ID: {cave['cave_id']}, Name: {cave['nom']}")

def list_etageres(cave_id):
    etageres = Etagere.get_etageres_by_cave(cave_id)
    for etagere in etageres:
        print(f"Etagere ID: {etagere['etagere_id']}, Number: {etagere['num_etagere']}")

def list_bottles(etagere_id):
    bouteilles = Bouteille.get_bouteilles_by_etagere(etagere_id)
    for bouteille in bouteilles:
        print(f"Bottle ID: {bouteille['bouteille_id']}, Name: {bouteille['nom']}, Domaine: {bouteille['domaine']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wine Cellar Management CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add cave
    parser_add_cave = subparsers.add_parser("add_cave", help="Add a new cave")
    parser_add_cave.add_argument("user_id", type=int, help="ID of the user")
    parser_add_cave.add_argument("nom", type=str, help="Name of the cave")

    # Delete cave
    parser_delete_cave = subparsers.add_parser("delete_cave", help="Delete a cave")
    parser_delete_cave.add_argument("cave_id", type=int, help="ID of the cave to delete")

    # Add etagere
    parser_add_etagere = subparsers.add_parser("add_etagere", help="Add a new etagere")
    parser_add_etagere.add_argument("cave_id", type=int, help="ID of the cave")
    parser_add_etagere.add_argument("num_etagere", type=int, help="Number of the etagere")
    parser_add_etagere.add_argument("emplacements", type=int, help="Number of available emplacements")

    # Delete etagere
    parser_delete_etagere = subparsers.add_parser("delete_etagere", help="Delete an etagere")
    parser_delete_etagere.add_argument("etagere_id", type=int, help="ID of the etagere to delete")

    # Add bottle
    parser_add_bottle = subparsers.add_parser("add_bottle", help="Add a new bottle")
    parser_add_bottle.add_argument("etagere_id", type=int, help="ID of the etagere")
    parser_add_bottle.add_argument("domaine", type=str, help="Domaine of the wine")
    parser_add_bottle.add_argument("nom", type=str, help="Name of the wine")
    parser_add_bottle.add_argument("typeVin", type=str, help="Type of the wine")
    parser_add_bottle.add_argument("region", type=str, help="Region of the wine")
    parser_add_bottle.add_argument("annee", type=int, help="Year of the wine")
    parser_add_bottle.add_argument("prix", type=float, help="Price of the wine")
    parser_add_bottle.add_argument("photo", type=str, help="Photo of the bottle")
    parser_add_bottle.add_argument("quantite", type=int, help="Quantity of the bottles")

    # Delete bottle
    parser_delete_bottle = subparsers.add_parser("delete_bottle", help="Delete a bottle")
    parser_delete_bottle.add_argument("bouteille_id", type=int, help="ID of the bottle to delete")

    # List caves
    parser_list_caves = subparsers.add_parser("list_caves", help="List all caves of a user")
    parser_list_caves.add_argument("user_id", type=int, help="ID of the user")

    # List etageres
    parser_list_etageres = subparsers.add_parser("list_etageres", help="List all etageres of a cave")
    parser_list_etageres.add_argument("cave_id", type=int, help="ID of the cave")

    # List bottles
    parser_list_bottles = subparsers.add_parser("list_bottles", help="List all bottles in an etagere")
    parser_list_bottles.add_argument("etagere_id", type=int, help="ID of the etagere")

    args = parser.parse_args()

    if args.command == "add_cave":
        add_cave(args.user_id, args.nom)
    elif args.command == "delete_cave":
        delete_cave(args.cave_id)
    elif args.command == "add_etagere":
        add_etagere(args.cave_id, args.num_etagere, args.emplacements)
    elif args.command == "delete_etagere":
        delete_etagere(args.etagere_id)
    elif args.command == "add_bottle":
        add_bottle(args.etagere_id, args.domaine, args.nom, args.typeVin, args.region, args.annee, args.prix, args.photo, args.quantite)
    elif args.command == "delete_bottle":
        delete_bottle(args.bouteille_id)
    elif args.command == "list_caves":
        list_caves(args.user_id)
    elif args.command == "list_etageres":
        list_etageres(args.cave_id)
    elif args.command == "list_bottles":
        list_bottles(args.etagere_id)
    else:
        parser.print_help()
