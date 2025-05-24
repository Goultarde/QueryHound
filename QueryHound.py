import json
import os
import subprocess
import argparse
import readline

def get_user_input(prompt, default=None):
    if default:
        return input(f"{prompt} [{default}]: ") or default
    else:
        return input(prompt)

def load_existing_queries_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
                return data.get("queries", [])
            except json.JSONDecodeError:
                print(f"Le fichier {file_path} n'est pas un JSON valide.")
                return []
    else:
        print(f"Fichier non trouvé : {file_path}")
        return []

def choose_load_mode():
    while True:
        print("Comment veux-tu démarrer ?")
        print("1. Charger les queries depuis custom_queries.json (si présent)")
        print("2. Charger les queries depuis un autre fichier JSON")
        print("3. Commencer avec une nouvelle liste vide")

        choice = get_user_input("Choix (1/2/3) : ", "1").strip()

        if choice == "1":
            if os.path.exists("custom_queries.json"):
                return load_existing_queries_from_file("custom_queries.json")
            else:
                print("Fichier custom_queries.json introuvable. Veuillez choisir une autre option.")
        elif choice == "2":
            path = get_user_input("Chemin du fichier JSON à charger : ").strip()
            if os.path.exists(path):
                return load_existing_queries_from_file(path)
            else:
                print(f"Fichier non trouvé : {path}. Veuillez choisir une autre option.")
        elif choice == "3":
            return []
        else:
            print("Choix invalide. Réessaye.")

def display_queries_pager(queries):
    output = "\nSummary of queries to be generated:\n"
    for i, query in enumerate(queries, start=1):
        output += f"\nQuery {i}:\n"
        output += f"  Name: {query['name']}\n"
        output += f"  Category: {query['category']}\n"
        output += "  Sub-queries:\n"
        for j, sub_query in enumerate(query['queryList'], start=1):
            output += f"    {j}. Query: {sub_query['query']}\n"
            output += f"       Final: {sub_query['final']}\n"

    try:
        less = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE)
        less.communicate(input=output.encode('utf-8'))
    except FileNotFoundError:
        print(output)

def create_query():
    query = {}
    query["name"] = get_user_input("Enter the query name: ")
    query["category"] = get_user_input("Enter the query category: ")
    query["queryList"] = []

    while True:
        sub_query = {}
        sub_query["query"] = get_user_input("Enter the query: ")

        if query["queryList"]:
            query["queryList"][-1]["final"] = False

        sub_query["final"] = True
        query["queryList"].append(sub_query)

        add_another = get_user_input("Do you want to add another sub-query? (y/N): ", "N").strip().lower()
        if add_another != 'y':
            break

    return query

def display_queries(queries):
    print("\nSummary of queries to be generated:")
    for i, query in enumerate(queries, start=1):
        print(f"\nQuery {i}:")
        print(f"  Name: {query['name']}")
        print(f"  Category: {query['category']}")
        print("  Sub-queries:")
        for j, sub_query in enumerate(query['queryList'], start=1):
            print(f"    {j}. Query: {sub_query['query']}")
            print(f"       Final: {sub_query['final']}")

def edit_query(query):
    while True:
        print("\nEditing Query:")
        print(f"  Name: {query['name']}")
        print(f"  Category: {query['category']}")
        print("  Sub-queries:")
        for j, sub_query in enumerate(query['queryList'], start=1):
            print(f"    {j}. Query: {sub_query['query']}")
            print(f"       Final: {sub_query['final']}")

        action = get_user_input("\nChoose an action: edit name (n), edit category (c), edit sub-query (s), or finish (f): ", "f").strip().lower()

        if action == 'n':
            query["name"] = get_user_input("Enter the new query name: ")
        elif action == 'c':
            query["category"] = get_user_input("Enter the new query category: ")
        elif action == 's':
            try:
                sub_query_index = int(get_user_input("Enter the sub-query number to edit: ")) - 1
                if 0 <= sub_query_index < len(query["queryList"]):
                    query["queryList"][sub_query_index]["query"] = get_user_input("Enter the new query: ")
                    query["queryList"][sub_query_index]["final"] = get_user_input("Is this the final query? (y/N): ", "N").strip().lower() == 'y'
                else:
                    print("Invalid sub-query number.")
            except ValueError:
                print("Please enter a valid number.")
        elif action == 'f':
            break
        else:
            print("Invalid action.")


def generate_custom_queries(args):
    # Chargement des queries selon option --default
    if args.default:
        if os.path.exists("custom_queries.json"):
            queries = load_existing_queries_from_file("custom_queries.json")
        else:
            queries = []
    else:
        queries = choose_load_mode()
        # Pose la question uniquement si on n'est PAS en mode summary
        if not args.summary:
            show_summary = get_user_input("Afficher le résumé des queries avant l’édition ? (y/N) : ", "N").strip().lower()
            if show_summary == 'y':
                display_queries_pager(queries)

    # Gestion des options passées en ligne de commande
    if args.summary:
        # Affiche résumé puis quitte sans sauvegarder
        if queries:
            display_queries_pager(queries)
        else:
            print("Aucune query à afficher.")
        return  # Quitte après résumé

    if args.action == "edit":
        # Affiche résumé pour choisir
        if queries:
            display_queries_pager(queries)
            try:
                query_number = int(get_user_input("Entrez le numéro de la query à éditer : "))
                if 0 < query_number <= len(queries):
                    edit_query(queries[query_number - 1])
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        else:
            print("Aucune query à éditer.")
    elif args.action == "remove":
        # Affiche résumé pour choisir
        if queries:
            display_queries_pager(queries)
            try:
                query_number = int(get_user_input("Entrez le numéro de la query à supprimer : "))
                if 0 < query_number <= len(queries):
                    del queries[query_number - 1]
                    print(f"Query {query_number} supprimée.")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        else:
            print("Aucune query à supprimer.")
    elif args.action == "add":
        query = create_query()
        queries.append(query)

    # Si on est arrivé ici, on lance la boucle d’interaction normale
    while True:
        action = get_user_input(
            "\nDo you want to add, edit, remove a query, show summary, or finish? (add[a]/edit[e]/remove[r]/summary[s]/done[d]): ",
            "done"
        ).strip().lower()

        if action in ['add', 'a']:
            query = create_query()
            queries.append(query)
        elif action in ['edit', 'e']:
            if queries:
                display_queries_pager(queries)
                try:
                    query_number = int(get_user_input("Enter the number of the query to edit: "))
                    if 0 < query_number <= len(queries):
                        edit_query(queries[query_number - 1])
                    else:
                        print("Invalid query number.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("No queries to edit.")
        elif action in ['remove', 'r']:
            if queries:
                display_queries_pager(queries)
                try:
                    query_number = int(get_user_input("Enter the number of the query to remove: "))
                    if 0 < query_number <= len(queries):
                        del queries[query_number - 1]
                        print(f"Query {query_number} removed.")
                    else:
                        print("Invalid query number.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("No queries to remove.")
        elif action in ['summary', 's']:
            if queries:
                display_queries_pager(queries)
            else:
                print("No queries to display.")
        elif action in ['done', 'd', '']:
            break
        else:
            print("Invalid action.")

    # Sauvegarde automatique dans custom_queries.json (option par défaut)
    output_file = "custom_queries.json"
    custom_queries_json = {
        "queries": queries
    }
    with open(output_file, "w") as json_file:
        json.dump(custom_queries_json, json_file, indent=4)

    print(f"Fichier JSON sauvegardé avec succès dans '{output_file}' !")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QueryHound - Gestionnaire de queries BloodHound.")
    parser.add_argument('--add', '-a', action='store_const', const='add', dest='action', help='Ajouter une query')
    parser.add_argument('--edit', '-e', action='store_const', const='edit', dest='action', help='Éditer une query')
    parser.add_argument('--remove', '-r', action='store_const', const='remove', dest='action', help='Supprimer une query')
    parser.add_argument('--default', '-d', action='store_true', help='Démarrer sans demander comment charger ni afficher le résumé')
    parser.add_argument('--summary', '-s', action='store_true', help='Afficher le résumé puis quitter sans sauvegarder')

    args = parser.parse_args()
    generate_custom_queries(args)

