# bot.py

####### IDEE : EVALUER LES ECHANGES ET LES PERSONNES
####### IDEE : PERMETTRE A CERTAINS ROLE D'ACCEDER A DES ECHANGES PLUS TOT QUE D'AUTRES

import discord
from discord.ext import commands
from discord import app_commands
import logging

from cards import Card, available_cards, User
from config import COMMAND_PREFIX, SERVER_ID, TOKEN

import json
import os

USERS_FILE = 'user_data.json'

def save_users(users):
    with open('users.json', 'w') as file:
        users_data = {}
        for user_id, user in users.items():
            users_data[user_id] = {
                "username": user.username,
                "searches": [card.card_number for card in user.searches],
                "trades": [card.card_number for card in user.trades]
            }
        json.dump(users_data, file)


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
    return users


def find_card_by_number(card_number):
    for card in available_cards:
        if card.card_number == card_number:
            return card
    return None  # or raise an exception if a card with the given number doesn't exist



def get_or_create_user(users: dict, user_id: str, username: str) -> User:
    user = users.get(user_id)
    if user is None:
        user = User(username)
        users[user_id] = user
    return user


# Configuration de la journalisation vers un fichier
logging.basicConfig(filename='bot.log', level=logging.INFO)
if not logging.getLogger().handlers:
    logging.error("La configuration de la journalisation a échoué.")

# On initialise l'objet discord.Intents avec toutes les intentions
intents = discord.Intents.all()
# On initialise le bot avec un préfixe de commande et les intentions précédemment définies
bot = commands.Bot(command_prefix=COMMAND_PREFIX,intents=intents)

# Initialisation du client
class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False # On utilise cette variable pour vérifier si les commandes ont été synchronisées 

    async def on_ready(self):
        # La méthode on_ready est appelée lorsque le bot est prêt
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            try:
                await tree.sync(guild = discord.Object(id=SERVER_ID)) #guild specific: leave blank if global (global registration can take 1-24 hours)
                self.synced = True
                logging.info(f"We have logged in as {self.user}.")
                print(f"Le bot {self.user} est prêt.")
                print(f"Nous sommes connecté en tant que {self.user}.")
            except Exception as e:
                logging.error("La synchronisation des commandes a échoué :", exc_info=True)
                print("La synchronisation des commandes a échoué :", e)
client = aclient() # On initialise le client
tree = app_commands.CommandTree(client) # On initialise l'arbre de commande

users = {}  # Dictionnaire pour stocker les informations des utilisateurs
cards_available = {}  # Dictionnaire pour stocker les cartes disponibles


# Commande pour afficher les commandes disponibles
@tree.command(guild = discord.Object(id=SERVER_ID), name = 'help_trade', description='Liste des commandes disponibles') 
async def help_trade(interaction: discord.Interaction):
    # Définition des commandes et leurs descriptions pour le bot
    embed = discord.Embed(title="Liste des commandes", description="Voici une liste des commandes que vous pouvez utiliser :", color=discord.Color.blue())
    embed.add_field(name="/show_available_cards", value="Afficher toutes les cartes disponibles.", inline=False)
    embed.add_field(name="/show_selected_cards [card_identifiers]", value="Afficher les cartes spécifiées par leurs identifiants.", inline=False)
    embed.add_field(name="/search_card [card_identifier]", value="Rechercher une carte spécifique par son identifiant.", inline=False)
    embed.add_field(name="/search_card_for_trade [card_identifier] [trade_cards]", value="Rechercher une carte à échanger contre d'autres cartes.", inline=False)
    embed.add_field(name="/trade_cards [trade_cards]", value="Proposer des cartes en échange.", inline=False)
    embed.add_field(name="/show_trades [cards]", value="Afficher les échanges en cours pour des cartes spécifiées.", inline=False)
    embed.add_field(name="/reset", value="Réinitialiser les recherches et échanges de l'utilisateur.", inline=False)
    embed.add_field(name="/remove_card [card_identifiers]", value="Supprimer une ou plusieurs cartes des recherches/échanges de l'utilisateur.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Commande pour afficher les cartes disponibles
@tree.command(guild=discord.Object(id=SERVER_ID), name='show_available_cards', description='Liste l\'ensemble des cartes')
async def show_available_cards(interaction: discord.Interaction):
    try:
        logging.info("La commande /show_available_cards a été exécutée.")
        cards_list = []
        for card in available_cards:
            cards_list.append(f"Carte N° {card.card_number}, Nom: {card.name}, Rareté: {card.rarity}")

        if not cards_list:
            await interaction.response.send_message("Aucune carte disponible.", ephemeral=True)
            return

        await interaction.response.send_message("Voici la liste des cartes disponibles :", ephemeral=True)

        # Envoie des messages avec les cartes disponibles
        for chunk in chunks(cards_list, 10):
            message = "\n".join(chunk)
            await interaction.followup.send(message, ephemeral=True)
    except Exception as e:
        logging.error("La commande /show_available_cards a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Divise une liste en morceaux de taille n.
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Commande pour afficher les cartes spécifiées
@tree.command(guild = discord.Object(id=SERVER_ID), name = 'show_selected_cards', description='Permet d\'afficher une ou plusieurs cartes particulière')
async def show_selected_cards(interaction: discord.Interaction, card_identifiers: str):
    try:
        logging.info("La commande /show_selected_cards a été exécutée.")
        if not card_identifiers:
            await interaction.response.send_message("Veuillez spécifier au moins une carte.", ephemeral=True)
            return

        card_identifiers = [card_identifier.strip() for card_identifier in card_identifiers.split(',')]


        cards_info = []
        for card_identifier in card_identifiers:
            card_identifier = card_identifier.strip()  # remove leading/trailing white spaces
            card_info = get_card_information(card_identifier)
            if card_info:
                cards_info.append(card_info)

        if cards_info:
            await interaction.response.send_message("Voici les informations de vos cartes :")  # initial response
            for card in cards_info:
                embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
                embed.set_image(url=card.image_url)
                await interaction.followup.send(embed=embed, ephemeral=True)  # follow-up messages for each card
        else:
            await interaction.response.send_message("Aucune carte trouvée.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /show_selected_cards a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Fonction pour obtenir les informations de la carte en fonction de son identifiant
def get_card_information(card_identifier):
    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            return card
    return None


# Commande pour rechercher une carte spécifique
@tree.command(guild=discord.Object(id=SERVER_ID), name='search_card', description='Permet de signaler que vous recherchez une carte')
async def search_card(interaction: discord.Interaction, card_identifiers: str):
    try:
        logging.info("La commande /search_card a été exécutée.")
        
        users = load_users()

        user = get_or_create_user(users, str(interaction.user.id), interaction.user.name)

        card_identifiers = [identifier.strip() for identifier in card_identifiers.split(',')]

        cards_info = []
        for card_identifier in card_identifiers:
            card_found = False

            for card in available_cards:
                if card.card_number == card_identifier.strip().lower() or (card.name.strip().lower() + " " + card.rarity.strip().lower()) == card_identifier.strip().lower():
                    if any(card_identifier == search.card_number for search in user.searches):
                        await interaction.response.send_message("Tu recherches déjà la carte " + card_identifier, ephemeral=True)
                        card_found = True
                        break

                    user.searches.append(card)
                    cards_info.append(card)
                    card_found = True

            if not card_found:
                await interaction.response.send_message(f"La carte spécifiée '{card_identifier}' n'existe pas.", ephemeral=True)

        save_users(users)

        if cards_info:
            embed = discord.Embed(title="Cartes recherchées", color=discord.Color.blue())
            for card in cards_info:
                embed.add_field(name=card.name, value=card.rarity, inline=False)
            await interaction.response.send_message(f"{interaction.user.mention} recherche :", embed=embed)
    except Exception as e:
        logging.error("La commande /search_card a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour rechercher une carte spécifique en échange d'autres cartes spécifiées
@tree.command(guild=discord.Object(id=SERVER_ID), name='search_card_for_trade', description='Permet de rechercher une carte en échange d\'autres cartes spécifiées')
async def search_card_for_trade(interaction: discord.Interaction, card_to_search: str, trade_all_cards: bool, trade_cards: str):
    try:
        logging.info("La commande /search_card a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user = get_or_create_user(users, str(interaction.user.id), interaction.user.name)

        card_to_search = card_to_search.strip().lower()

        trade_cards = [card.strip() for card in trade_cards.split(',')]

        main_card = None
        trade_cards_list = []

        for card in available_cards:
            if card.card_number == card_to_search or (card.name + " " + card.rarity).lower() == card_to_search.lower():
                main_card = card
                break

        if main_card is None:
            await interaction.response.send_message(f"La carte spécifiée '{card_to_search}' n'existe pas.", ephemeral=True)
            return

        for trade_card in trade_cards:
            for card in available_cards:
                if card.card_number == trade_card.strip().lower() or (card.name.strip().lower() + " " + card.rarity.strip().lower()) == trade_card.strip().lower():
                    trade_cards_list.append(card)
                    break

        if not trade_cards_list:
            await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.", ephemeral=True)
            return

        user.searches.append(main_card)
        user.trades.extend(trade_cards_list)

        save_users(users)  # Enregistrer les utilisateurs dans le fichier JSON

        embed = discord.Embed(title="Recherche de carte en échange", color=discord.Color.blue())
        embed.add_field(name="Carte recherchée", value=main_card.name, inline=False)

        trade_description = "\n".join([card.name for card in trade_cards_list])
        embed.add_field(name="Cartes proposées en échange", value=trade_description, inline=False)

        if trade_all_cards:
            embed.add_field(name="Proposition", value="Toutes les cartes affichées sont proposées en échange.", inline=False)
        else:
            embed.add_field(name="Proposition", value="Une carte parmi les cartes affichées est proposée en échange.", inline=False)

        await interaction.response.send_message(f"{interaction.user.mention} recherche :", embed=embed)
    except Exception as e:
        logging.error("La commande /search_card_for_trade a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour proposer des cartes en échange
@tree.command(guild=discord.Object(id=SERVER_ID), name='trade_cards', description='Permet de signaler que vous avez une ou des cartes à échanger')
async def trade_cards(interaction: discord.Interaction, trade_cards: str):
    try:
        logging.info("La commande /trade_cards a été exécutée.")
        
        users = load_users()

        user = get_or_create_user(users, str(interaction.user.id), interaction.user.name)

        trade_cards_list = [card.strip() for card in trade_cards.split(',')]

        for card_identifier in trade_cards_list:
            card_info = next((card for card in available_cards if card.card_number == card_identifier or (card.name + " " + card.rarity).lower() == card_identifier.lower()), None)
            if card_info:
                user.trades.append(card_info)

        save_users(users)

        if not user.trades:
            await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.", ephemeral=True)
            return

        embed = discord.Embed(title="Cartes proposées en échange", description="Voici les cartes que vous proposez en échange :", color=discord.Color.blue())
        for card in user.trades:
            embed.add_field(name=card.name, value=card.rarity, inline=False)
        await interaction.response.send_message(f"{interaction.user.mention} propose en échange :", embed=embed)
    except Exception as e:
        logging.error("La commande /trade_cards a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)



## PROBLEME LA COMMANDE NE RENVOIE PAS DE RESULTAT LORSQU'ON SPECIFIE UNE CARTE PAR SON NUMERO
# Commande pour afficher les échanges en cours
@tree.command(guild=discord.Object(id=SERVER_ID), name='show_trades', description='Affiche les propositions de cartes en cours')
async def show_trades(interaction: discord.Interaction, cards: str = ""):
    try:
        logging.info("La commande /show_trades a été exécutée.")
        if cards:
            cards = [card.strip() for card in cards.split(",")]

        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        if cards:
            # Cas où des cartes sont spécifiées
            trades = []
            for user in users.values():
                for trade in user.trades:
                    card_info = next((card for card in available_cards if card.card_number == trade or card.name.lower() in trade.lower()), None)
                    print(card_info)
                    if card_info and any(card.lower() == trade.lower() or card.card_number.lower() == trade.lower() or (isinstance(card_info, Card) and card.lower() in card_info.name.lower() or card.lower() in card_info.rarity.lower()) for card in cards):
                        trades.append(f"{user.username} propose : {card_info.name} ({card_info.rarity})")

            if trades:
                embed = discord.Embed(title="Échanges concernant les cartes spécifiées", color=discord.Color.blue())
                embed.description = "\n".join(trades)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Il n'y a pas d'échanges en cours pour les cartes spécifiées.", ephemeral=True)
        else:
            # Cas où aucune carte n'est spécifiée
            trades = []
            for user in users.values():
                if user.trades:
                    for trade in user.trades:
                        card_info = next((card for card in available_cards if str(card.card_number) == trade or card.name.lower() in trade.lower()), None)
                        if card_info:
                            trades.append(f"{user.username} propose : {card_info.name} ({card_info.rarity})")

            if trades:
                embed = discord.Embed(title="Liste de tous les échanges en cours", color=discord.Color.blue())
                embed.description = "\n".join(trades)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Il n'y a pas d'échanges en cours.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /show_trades a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour réinitialiser les recherches et échanges de l'utilisateur
@tree.command(guild=discord.Object(id=SERVER_ID), name='reset', description='Réinitialiser les recherches et échanges de l\'utilisateur')
async def reset(interaction: discord.Interaction, reset_searches: bool = False, reset_trades: bool = False):
    try:
        logging.info("La commande /reset a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user = users.get(str(interaction.user.id))
        if user is None or (not user.searches and not user.trades):
            await interaction.response.send_message("Vous n'avez pas encore d'informations d'utilisateur enregistrées.", ephemeral=True)
            return

        if reset_searches == False and reset_trades == False:
            user.reset()
            reset_message = "Vos recherches et échanges ont été réinitialisés avec succès."
        elif reset_searches:
            user.searches = []
            reset_message = "Vos recherches ont été réinitialisées avec succès."
        elif reset_trades:
            user.trades = []
            reset_message = "Vos échanges ont été réinitialisés avec succès."
        else:
            reset_message = "Aucune réinitialisation n'a été effectuée."

        save_users(users)  # Enregistrer les utilisateurs dans le fichier JSON

        await interaction.response.send_message(reset_message, ephemeral=True)
    except Exception as e:
        logging.error("La commande /reset a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


@tree.command(guild=discord.Object(id=SERVER_ID), name='remove_card', description='Supprimer une ou plusieurs cartes de vos recherches/échanges')
async def remove_card(interaction: discord.Interaction, card_identifiers: str):
    try:
        logging.info("La commande /remove_card a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user_id = str(interaction.user.id)
        user = users.get(user_id)
        if user is None or (not user.searches and not user.trades):
            await interaction.response.send_message("Vous n'avez pas encore d'informations d'utilisateur enregistrées.", ephemeral=True)
            return

        card_identifiers = [card.strip() for card in card_identifiers.split(',')]

        removed_searches = []
        removed_trades = []

        for card_identifier in card_identifiers:
            removed_searches.extend([search for search in user.searches if search.card_number == card_identifier.strip().lower() or (search.name.strip().lower() + " " + search.rarity.strip().lower()) == card_identifier.strip().lower()])
            removed_trades.extend([trade for trade in user.trades if trade.card_number == card_identifier.strip().lower() or (trade.name.strip().lower() + " " + trade.rarity.strip().lower()) == card_identifier.strip().lower()])

        user.searches = [search for search in user.searches if search not in removed_searches]
        user.trades = [trade for trade in user.trades if trade not in removed_trades]

        save_users(users)  # Enregistrer les utilisateurs dans le fichier JSON

        if removed_searches or removed_trades:
            await interaction.response.send_message("Les cartes spécifiées ont été supprimées de vos recherches/échanges avec succès.", ephemeral=True)
        else:
            await interaction.response.send_message("Aucune carte correspondante n'a été trouvée dans vos recherches/échanges.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /remove_card a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)



# Connecte le bot au serveur
client.run(TOKEN)