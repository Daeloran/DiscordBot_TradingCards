import json

USERS_FILE = "users.json"
print(USERS_FILE)

def update_users_file_score():
    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)

        for user_id, user_data in users.items():
            if "score" not in user_data:
                user_data["score"] = 0

        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

        print("Mise à jour du fichier users.json terminée.")
    except FileNotFoundError:
        print("Le fichier users.json n'a pas été trouvé.")

# Appel de la fonction pour mettre à jour le fichier users.json
#update_users_file()


def update_users_file_rating():
    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)

        for user_id, user_data in users.items():
            if "ratings" not in user_data:
                user_data["ratings"] = []

        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

        print("Mise à jour du fichier users.json terminée.")
    except FileNotFoundError:
        print("Le fichier users.json n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur s'est produite lors de la mise à jour du fichier users.json:", str(e))

# Appel de la fonction pour mettre à jour le fichier users.json
update_users_file_rating()


