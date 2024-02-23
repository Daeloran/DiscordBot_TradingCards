# bot.py

import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole, NoPrivateMessage
from discord import app_commands
import logging
import random

from classes import Evaluation
from cards import available_cards
from functions import *
from config import COMMAND_PREFIX, SERVER_ID, TOKEN


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
                #await tree.sync()
                self.synced = True
                logging.info(f"We have logged in as {self.user}.")
                print(f"Le bot {self.user} est prêt.")
                print(f"Nous sommes connecté en tant que {self.user}.")
                #asyncio.create_task(send_notifications(self))  # On crée une tâche asynchrone pour envoyer les notifications
            except Exception as e:
                logging.error("La synchronisation des commandes a échoué :", exc_info=True)
                print("La synchronisation des commandes a échoué :", e)

client = aclient() # On initialise le client
tree = app_commands.CommandTree(client) # On initialise l'arbre de commande

users = {}  # Dictionnaire pour stocker les informations des utilisateurs
cards_available = {}  # Dictionnaire pour stocker les cartes disponibles

async def direct_message(user, message):
    to = await client.fetch_user(int(user))
    if to:
        #print('sending message to', to)
        await to.send(message)

@tree.command(guild=discord.Object(id=SERVER_ID), name='secret', description='Vous envoie un message secret')
async def secret(interaction: discord.Interaction):
    messages = [
        "Hey ! Juste un petit message pour te dire que tu es fantastique et que tu rends ce monde meilleur.",
        "Salut ! Tu as un sourire radieux qui illumine la journée de chacun. Continue d'être toi-même, c'est génial !",
        "Coucou ! Savais-tu que tu es une source d'inspiration pour beaucoup de personnes ? Continue de briller et de faire la différence !",
        "Bonjour ! Aujourd'hui est une journée spéciale parce que tu es là. N'oublie pas à quel point tu es important et aimé(e) !",
        "Salut toi ! Tu es unique et précieux/precieuse. Ne laisse jamais personne te faire douter de ta valeur. Sois fier/fière de qui tu es !"
    ]
    
    interaction = await interaction.user.create_dm()
    message = random.choice(messages)
    await interaction.send(message)

# Commande pour afficher les commandes disponibles
@tree.command(guild=discord.Object(id=SERVER_ID), name='help_trade', description='Liste des commandes disponibles') 
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
    embed.add_field(name="/profile", value="Affiche votre profile permettant de visualiser vos cartes recherchées/proposée, votre score, etc", inline=False)
    embed.add_field(name="/leaderboad", value="Affiche le classement des échanges", inline=False)
    embed.add_field(name="/stats", value="Affiche le nombre de recherches et de proposition en cours", inline=False)
    embed.add_field(name="/delete_profile", value="Supprime totalement votre profile du bot.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Commande pour afficher les cartes disponibles
@tree.command(guild=discord.Object(id=SERVER_ID), name='show_available_cards', description='Liste l\'ensemble des cartes')
async def show_available_cards(interaction: discord.Interaction):
    try:
        logging.info("La commande /show_available_cards a été exécutée.")
        cards_list = []
        for card in available_cards:
            cards_list.append(f"Carte # {card.card_number}, Nom: {card.name}, Rareté: {card.rarity}")

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

### MODIFIER AFFICHAGE DU EMBED
# Commande pour afficher les cartes spécifiées
@tree.command(guild=discord.Object(id=SERVER_ID), name='show_selected_cards', description='Permet d\'afficher une ou plusieurs cartes particulière')
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
            await interaction.response.send_message("Voici les informations de la cartes :", ephemeral=True)  # initial response
            for card in cards_info:
                embed = discord.Embed(title=card.name, description=f"# {card.card_number}\nRareté : {card.rarity}", color=discord.Color.blue())
                embed.set_image(url=card.image_url)
                await interaction.followup.send(embed=embed, ephemeral=True)  # follow-up messages for each card
        else:
            await interaction.response.send_message("Aucune carte trouvée.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /show_selected_cards a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


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
            embeds = build_card_info_embeds(cards_info)

            for index, embed in enumerate(embeds):
                if index == 0:
                    await interaction.response.send_message(f"{interaction.user.mention} recherche :", embed=embed)
                else:
                    await interaction.followup.send(f"{interaction.user.mention} recherche :", embed=embed)
        
        # Appeler la fonction notifications pour rechercher les utilisateurs proposant les cartes spécifiées
        notified_users = await notifications(cards_info, interaction.user, "trade")

        # Créer le message de notification dans le canal avec les utilisateurs notifiés
        if notified_users:
            users_mentions = " ".join(f"<@{user_id}>" for user_id in notified_users)
            await interaction.followup.send(f"{users_mentions}, {interaction.user.mention} recherche des cartes et tu pourrais l'aider !")


    except Exception as e:
        logging.error("La commande /search_card a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


### A OPTIMISER POUR NE PAS AVOIR A PARCOURIR LA LISTE DE TOUTE LES CARES A CHAQUE FOIS
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

        points = 0

        for trade_card in trade_cards:
            for card in available_cards:
                if card.card_number == trade_card.strip().lower() or (card.name.strip().lower() + " " + card.rarity.strip().lower()) == trade_card.strip().lower():
                    trade_cards_list.append(card)
                    # Calculer les points et les ajouter au score de l'utilisateur
                    points = calculate_points(card.rarity) # Calculer les points de la carte
                    break
        if trade_all_cards:
            user.score += points * len(trade_cards)  # Ajouter les points multipliés par le nombre de cartes proposées en échange
        else: 
            user.score += points / len(trade_cards)  # Ajouter les points divisés par le nombre de cartes proposées en échange

        if not trade_cards_list:
            await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.", ephemeral=True)
            return

        user.searches.append(main_card)
        user.trades.extend(trade_cards_list)

        save_users(users)  # Enregistrer les utilisateurs dans le fichier JSON

        embed = discord.Embed(title="Recherche de carte en échange", color=discord.Color.blue())
        embed.add_field(name="Carte recherchée", value=f"# {main_card.card_number} : {main_card.name}\n", inline=False)

        trade_description = "\n".join([f"# {card.card_number} : {card.name}" for card in trade_cards_list])
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

        cards_info = []
        for card_identifier in trade_cards_list:
            card_info = next((card for card in available_cards if card.card_number == card_identifier or (card.name + " " + card.rarity).lower() == card_identifier.lower()), None)
            if card_info:
                user.trades.append(card_info)
                cards_info.append(card_info)
            # Calculer les points et les ajouter au score de l'utilisateur
            points = calculate_points(card_info.rarity)
            user.score += points

        save_users(users)

        if not user.trades:
            await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.", ephemeral=True)
            return


        embeds = build_card_info_embeds(cards_info)

        for index, embed in enumerate(embeds):
            embed.color = discord.Color.yellow()
            if index == 0:
                await interaction.response.send_message(f"{interaction.user.mention} propose en échange :", embed=embed)
            else:
                await interaction.followup.send(f"{interaction.user.mention} propose en échange :", embed=embed)

        # Appeler la fonction notifications pour rechercher les utilisateurs recherchant les cartes spécifiées
        notified_users = await notifications(cards_info, interaction.user, "search")

        # Créer le message de notification dans le canal avec les utilisateurs notifiés
        if notified_users:
            users_mentions = " ".join(f"<@{user_id}>" for user_id in notified_users)
            await interaction.followup.send(f"{users_mentions}, {interaction.user.mention} propose en échange des cartes interessantes !")

    except Exception as e:
        logging.error("La commande /trade_cards a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


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
                    #card_info = find_card_by_number(trade)
                    card_info = next((card for card in available_cards if
                    (str(card.card_number) == trade or card.name.lower() in trade.lower()) and
                    any((card.card_number.lower() == c.lower() or
                    (card.name.lower() + " " + card.rarity.lower()) == c.lower())
                    for c in cards)), None)
                    if card_info:
                        trades.append(f"{user.username} propose : # {card_info.card_number} {card_info.name} ({card_info.rarity})")

            if trades:
                embed = discord.Embed(title="Échanges concernant les cartes spécifiées", color=discord.Color.purple())
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
                            trades.append(f"{user.username} propose : # {card_info.card_number} {card_info.name} ({card_info.rarity})")

            description = "\n".join(trades)
            if len(description) > 4096:
                # Diviser le contenu en plusieurs parties
                parts = [description[i:i+4093] for i in range(0, len(description), 4093)]

                # Envoyer le premier embed en utilisant interaction.response.send_message()
                embed = discord.Embed(title="Liste de tous les échanges en cours", color=discord.Color.purple())
                embed.description = parts[0]
                await interaction.response.send_message(embed=embed, ephemeral=True)

                # Envoyer les embeds suivants en utilisant interaction.followup.send()
                for part in parts[1:]:
                    embed = discord.Embed(title="Liste de tous les échanges en cours", color=discord.Color.purple())
                    embed.description = part
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                # Envoyer un seul embed si la description n'a pas besoin d'être divisée
                embed = discord.Embed(title="Liste de tous les échanges en cours", color=discord.Color.purple())
                embed.description = description
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
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


# Commande pour afficher le profil utilisateur (recherches et échanges)
@tree.command(guild=discord.Object(id=SERVER_ID), name='profile', description='Affiche votre profil utilisateur')
async def profile(interaction: discord.Interaction):
    try:
        logging.info("La commande /profile a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user = users.get(str(interaction.user.id))
        if user is None:
            await interaction.response.send_message("Votre profil utilisateur n'existe pas.", ephemeral=True)
            return

        embeds = []

        # Construction des embeds paginés
        profile_embed = discord.Embed(title="Profil utilisateur", color=discord.Color.blue())
        profile_embed.add_field(name="Utilisateur", value=interaction.user.name, inline=False)
        embeds.append(profile_embed)

        # Construction des autres parties du profil utilisateur
        searches_embeds = build_searches_embeds(user.searches)
        trades_embeds = build_trades_embeds(user.trades)

        # Ajout des embeds de recherches et échanges
        embeds.extend(searches_embeds)
        embeds.extend(trades_embeds)

        # Envoi des embeds paginés
        for index, embed in enumerate(embeds):
            if index == 0:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        logging.error("La commande /profile a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour afficher le classement des utilisateurs
@tree.command(guild=discord.Object(id=SERVER_ID), name='leaderboard', description='Affiche le classement des utilisateurs')
async def leaderboard(interaction: discord.Interaction):
    try:
        logging.info("La commande /leaderboard a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        sorted_users = sorted(users.values(), key=lambda user: user.score, reverse=True)

        embed = discord.Embed(title="Classement des utilisateurs", color=discord.Color.blue())
        rank = 1
        for user in sorted_users:
            embed.add_field(name=f"#{rank} - {user.username}", value=f"Score : {user.score}", inline=False)
            rank += 1

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        logging.error("La commande /leaderboard a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour afficher les statistiques d'échange et de recherche en cours
@tree.command(guild=discord.Object(id=SERVER_ID), name='stats', description='Affiche les statistiques du bot')
async def stats(interaction: discord.Interaction):
    try:
        logging.info("La commande /stats a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        total_searches = sum(len(user.searches) for user in users.values())
        total_trades = sum(len(user.trades) for user in users.values())

        embed = discord.Embed(title="Statistiques du bot", color=discord.Color.purple())
        embed.add_field(name="Nombre de recherches en cours", value=total_searches, inline=False)
        embed.add_field(name="Nombre d'échanges en cours", value=total_trades, inline=False)

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        logging.error("La commande /stats a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


# Commande pour supprimer le profil utilisateur
@tree.command(guild=discord.Object(id=SERVER_ID), name='delete_profile', description='Supprime votre profil utilisateur')
async def delete_profile(interaction: discord.Interaction):
    try:
        logging.info("La commande /delete_profile a été exécutée.")
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user_id = str(interaction.user.id)
        if user_id in users:
            del users[user_id]
            save_users(users)
            await interaction.response.send_message("Votre profil utilisateur a été supprimé avec succès.", ephemeral=True)
        else:
            await interaction.response.send_message("Votre profil utilisateur n'existe pas.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /delete_profile a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


@tree.command(guild=discord.Object(id=SERVER_ID), name='rate_user', description='Permet d\'évaluer un utilisateur')
async def rate_user(interaction: discord.Interaction, evaluated_user: discord.Member, rating: int, comment: str = "", cards_sent: str = ""):
    try:
        logging.info("La commande /rate_user a été exécutée.")
        
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON
        
        evaluator_id = str(interaction.user.id)
        evaluator_username = interaction.user.name
        
        evaluated_user_id = str(evaluated_user.id)
        evaluated_username = evaluated_user.name

        if(evaluator_username == evaluated_username):
            logging.error("La commande /rate_user a échoué (auto_eval) :", exc_info=True)
            await interaction.response.send_message("Vous ne pouvez pas vous évaluer vous-même.", ephemeral=True)
            return
        
        # Vérifier si l'utilisateur évalué existe, sinon le créer
        if evaluated_user_id not in users:
            get_or_create_user(users, evaluated_user_id, evaluated_username)
        
        # Vérifier si l'utilisateur évaluant existe, sinon le créer
        if evaluator_id not in users:
            get_or_create_user(users, evaluator_id, evaluator_username)
        
        evaluated_user = users[evaluated_user_id]
               
        # Créer l'évaluation
        evaluation = Evaluation(evaluator_username, rating, comment, cards_sent.split(",") if cards_sent else [])
        
        # Ajouter l'évaluation à l'utilisateur évalué
        evaluated_user.add_evaluation(evaluation)
        
        # Enregistrer les utilisateurs dans le fichier JSON
        save_users(users)

        # Envoyer un message privé à l'utilisateur évalué pour confirmation
        confirmation_message = f"L'utilisateur {evaluator_username} vous a évalué."
        await direct_message(evaluated_user_id, confirmation_message)    
        
        await interaction.response.send_message(f"Vous avez évalué l'utilisateur {evaluated_username} avec une note de {rating}.", ephemeral=True)
        
    except Exception as e:
        logging.error("La commande /rate_user a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)

@tree.command(guild=discord.Object(id=SERVER_ID), name='show_evaluations', description='Affiche les évaluations d\'un utilisateur')
async def show_evaluations(interaction: discord.Interaction, username: discord.Member):
    try:
        logging.info("La commande /show_evaluations a été exécutée.")

        users = load_users()  # Charger les utilisateurs à partir du fichier JSON

        user_id = str(username.id)
        user = users.get(user_id)

        for user_data in users.values():
            if user_data.username == username:
                user = user_data
                break

        if user is None:
            await interaction.response.send_message(f"L'utilisateur '{username}' n'a pas d'évaluations.", ephemeral=True)
            return

        evaluations = user.evaluations
        if not evaluations:
            await interaction.response.send_message(f"L'utilisateur '{username}' n'a pas d'évaluations.", ephemeral=True)
            return

        embed = discord.Embed(title=f"Évaluations de l'utilisateur {username}", color=discord.Color.green())
        moyenne = 0

        for idx, evaluation in enumerate(evaluations):
            #cards_info = [f"Cartes échangées : {card.card_number} {card.name}" for card in evaluation.cards_sent]
            #print(cards_info)
            #embed.add_field(name=f"Évaluateur : {evaluation.evaluator_username}", value=f"Note : {evaluation.rating}/5\nCommentaire : {evaluation.comment}"+ "\n".join(cards_info), inline=False)
            embed.add_field(name=f"#{idx} Évaluateur : {evaluation.evaluator_username}", value=f"Note : {evaluation.rating}/5\nCommentaire : {evaluation.comment}", inline=False)
            moyenne += evaluation.rating

        moyenne = moyenne / len(evaluations)
        embed.add_field(name="Moyenne : ", value=f"{round(moyenne,2)}/5", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        logging.error("La commande /show_evaluations a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)


@tree.command(guild=discord.Object(id=SERVER_ID), name='remove_rate_user', description='ADMIN - Supprimer une évaluation un utilisateur')
async def rate_user(interaction: discord.Interaction, evaluated_user: discord.Member, id_eval: int):
    try:
        logging.info("La commande /remove_rate_user a été exécutée.")

        can_execute = False
        for role in interaction.user.roles:
            #1085684130425077851 Modo
            #1085684015014613083 Admin
            if role.id == 1085684130425077851 or role.id == 1085684015014613083: # check les roles modo et admin
                can_execute = True
                break
        if not can_execute:
            raise MissingAnyRole("Permission manquante")
        
        users = load_users()  # Charger les utilisateurs à partir du fichier JSON
        
        evaluated_user_id = str(evaluated_user.id)
        evaluated_username = evaluated_user.name
        
        evaluated_user = users[evaluated_user_id]

        # Supprime l'évaluation à l'utilisateur
        evaluated_user.remove_evaluation(evaluated_user.evaluations[id_eval])
        
        # Enregistrer les utilisateurs dans le fichier JSON
        save_users(users)
        
        await interaction.response.send_message(f"Vous avez supprimé une évalutaion de {evaluated_username}", ephemeral=True)
    except IndexError as e:
        logging.error("La commande /remove_rate_user a échoué (IndexError) :", exc_info=True)
        await interaction.response.send_message("L'index spécifié est invalide.", ephemeral=True)
    except MissingAnyRole as e:
        logging.error("La commande /remove_rate_user a échoué (permission) :", exc_info=True)
        await interaction.response.send_message("Vous n'avez pas la permission d'effectuer cette commande.", ephemeral=True)
    except Exception as e:
        logging.error("La commande /remove_rate_user a échoué :", exc_info=True)
        await interaction.response.send_message("Une erreur est survenue lors de l'exécution de la commande.", ephemeral=True)



# Connecte le bot au serveur
client.run(TOKEN)
