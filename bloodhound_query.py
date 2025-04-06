import json

def get_user_input(prompt):
    return input(prompt)

def create_query():
    query = {}
    query["name"] = get_user_input("Enter the query name: ")
    query["category"] = get_user_input("Enter the query category: ")
    query["queryList"] = []

    while True:
        sub_query = {}
        sub_query["final"] = get_user_input("Is this the final query? (true/false): ").strip().lower() == 'true'
        sub_query["query"] = get_user_input("Enter the query: ")

        if not sub_query["final"]:
            sub_query["title"] = get_user_input("Enter the title for this query: ")

        query["queryList"].append(sub_query)

        add_another = get_user_input("Do you want to add another sub-query? (yes/no): ").strip().lower()
        if add_another != 'yes':
            break

    return query

def generate_custom_queries():
    queries = []

    while True:
        query = create_query()
        queries.append(query)

        add_another_query = get_user_input("Do you want to add another query? (yes/no): ").strip().lower()
        if add_another_query != 'yes':
            break

    custom_queries_json = {
        "queries": queries
    }

    with open("custom_queries.json", "w") as json_file:
        json.dump(custom_queries_json, json_file, indent=4)

    print("Fichier JSON généré avec succès !")

# Appeler la fonction pour générer le fichier JSON
generate_custom_queries()

