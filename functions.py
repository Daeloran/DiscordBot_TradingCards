#function.py

import json
import os
import discord

from classes import User
from cards import available_cards
#from bot import aclient

USERS_FILE = 'user_data.json'

"""
=== Fonctions Utilisateur ===
"""
# Fonction pour enregistrer les utilisateurs dans le fichier JSON
def save_users(users):
    with open('users.json', 'w') as file:
        users_data = {}
        for user_id, user in users.items():
            users_data[user_id] = {
                "username": user.username,
                "searches": [card.card_number for card in user.searches],
                "trades": [card.card_number for card in user.trades],
                "score": user.score,  # Ajouter le score de l'utilisateur
            }
        json.dump(users_data, file)

# Fonction pour charger les utilisateurs à partir du fichier JSON
def load_users():
    if not os.path.exists('users.json') or os.stat('users.json').st_size == 0:
        return {}
    with open('users.json', 'r') as file:
        users_data = json.load(file)
    users = {}
    for user_id, user_data in users_data.items():
        user = User(user_data["username"])
        user.trades = [find_card_by_number(card_number) for card_number in user_data["trades"]]
        user.searches = [find_card_by_number(card_number) for card_number in user_data["searches"]]
        users[user_id] = user
        user.score = user_data["score"]  # Ajouter le score de l'utilisateur
    return users

# Fonction pour obtenir ou créer un utilisateur dans le dictionnaire des utilisateurs
def get_or_create_user(users: dict, user_id: str, username: str) -> User:
    user = users.get(user_id)
    if user is None:
        user = User(username)
        users[user_id] = user
        user.score = 0 # Initialiser le score à 0 lors de la création de l'utilisateur
    return user


"""
=== Fonctions Cartes ===
"""
# Fonction pour trouver une carte par son numéro
def find_card_by_number(card_number):
    for card in available_cards:
        if card.card_number == card_number:
            return card
    return None  # or raise an exception if a card with the given number doesn't exist

# Fonction pour obtenir les informations de la carte en fonction de son identifiant
def get_card_information(card_identifier):
    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            return card
    return None

# Fonction pour attribuer les points en fonction de la rareté de la carte
def calculate_points(rarity):
    if rarity == "Terrain":
        return 2
    elif rarity == "Commune":
        return 4
    elif rarity == "Peu Commune":
        return 6
    elif rarity == "Rare":
        return 10
    elif rarity == "Ultra rare holo 1":
        return 15
    elif rarity == "Ultra rare holo 2":
        return 20
    elif rarity == "Légendaire Bronze":
        return 30
    elif rarity == "Légendaire Argent":
        return 40
    elif rarity == "Légendaire Or":
        return 50
    else:
        return 0  # Gérer le cas d'une rareté inconnue si nécessaire


"""
=== Fonctions Embed ===
"""
def build_searches_embeds(searches):
    # Construire les embeds pour les recherches en cours
    searches_embeds = []
    current_embed = None
    for search in searches:
        if current_embed is None or len(current_embed.fields) >= 25:
            current_embed = discord.Embed(title="Recherches en cours", color=discord.Color.blue())
            searches_embeds.append(current_embed)

        current_embed.add_field(name=f"# {search.card_number}  {search.name}", value=f"{search.rarity}\n", inline=False)

    return searches_embeds

def build_trades_embeds(trades):
    # Construire les embeds pour les échanges en cours
    trades_embeds = []
    current_embed = None
    for trade in trades:
        if current_embed is None or len(current_embed.fields) >= 25:
            current_embed = discord.Embed(title="Cartes proposées en échange", color=discord.Color.blue())
            trades_embeds.append(current_embed)

        current_embed.add_field(name=f"# {trade.card_number}  {trade.name}", value=f"{trade.rarity}\n", inline=False)

    return trades_embeds

def build_card_info_embeds(cards_info):
    # Construire les embeds pour les informations des cartes
    embeds = []
    current_embed = None
    for card_info in cards_info:
        if current_embed is None or len(current_embed.fields) >= 25:
            current_embed = discord.Embed(title="Informations des cartes", color=discord.Color.blue())
            embeds.append(current_embed)

        current_embed.add_field(name=f"# {card_info.card_number}  {card_info.name}", value=f"{card_info.rarity}\n", inline=False)
        #current_embed.add_field(name="Rareté", value=card_info.rarity, inline=False)
        #current_embed.set_image(url=card_info.image_url)

    return embeds

# Divise une liste en morceaux de taille n.
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]




