import discord
from discord.ext import commands
from discord import app_commands
from cards import Card, available_cards, User

# On initialise l'objet discord.Intents avec toutes les intentions
intents = discord.Intents.all()
# On initialise le bot avec un préfixe de commande et les intentions précédemment définies
bot = commands.Bot(command_prefix='/',intents=intents)


####### IDEE : EVALUER LES ECHANGES ET LES PERSONNES
####### IDEE : PERMETTRE A CERTAINS ROLE D'ACCEDER A DES ECHANGES PLUS TOT QUE D'AUTRES

class aclient(discord.Client):
    # Initialisation du client
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False # On utilise cette variable pour vérifier si les commandes ont été synchronisées 

    async def on_ready(self):
        # La méthode on_ready est appelée lorsque le bot est prêt
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=1122893178278785175)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient() # On initialise le client
tree = app_commands.CommandTree(client) # On initialise l'arbre de commande

users = {}  # Dictionnaire pour stocker les informations des utilisateurs
cards_available = {}  # Dictionnaire pour stocker les cartes disponibles

# Commande pour afficher les commandes disponibles
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'help_trade', description='Liste des commandes disponibles') 
async def help_trade(interaction: discord.Interaction):
    # Définition des commandes et leurs descriptions pour le bot
    embed = discord.Embed(title="Liste des commandes", description="Voici une liste des commandes que vous pouvez utiliser :", color=discord.Color.blue())
    embed.add_field(name="/show_available_cards", value="Afficher toutes les cartes disponibles.", inline=False)
    embed.add_field(name="/show_selected_cards [card_identifiers]", value="Afficher les cartes spécifiées par leurs identifiants.", inline=False)
    embed.add_field(name="/search_card [card_identifier]", value="Rechercher une carte spécifique par son identifiant.", inline=False)
    embed.add_field(name="/search_card_for_trade [card_identifier] [trade_cards]", value="Rechercher une carte à échanger contre d'autres cartes.", inline=False)
    embed.add_field(name="/trade_cards [trade_cards]", value="Proposer des cartes en échange.", inline=False)
    embed.add_field(name="/show_trades [cards]", value="Afficher les échanges en cours pour des cartes spécifiées.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande pour afficher les cartes disponibles
@tree.command(guild=discord.Object(id=1122893178278785175), name='show_available_cards', description='Liste l\'ensemble des cartes')
async def show_available_cards(interaction: discord.Interaction):
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

def chunks(lst, n):
    """Divise une liste en morceaux de taille n."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Commande pour afficher les cartes spécifiées
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'show_selected_cards', description='Permet d\'afficher une ou plusieurs cartes particulière')
async def show_selected_cards(interaction: discord.Interaction, card_identifiers: str):
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


# Fonction pour obtenir les informations de la carte en fonction de son identifiant
def get_card_information(card_identifier):
    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            return card
    return None

# Commande pour rechercher une carte spécifique
@tree.command(guild=discord.Object(id=1122893178278785175), name='search_card', description='Permet de signaler que vous recherchez une carte')
async def search_card(interaction: discord.Interaction, card_identifiers: str):
    user = users.get(interaction.user.id)
    if user is None:
        user = User(interaction.user.name)
        users[interaction.user.id] = user

    card_identifiers = [identifier.strip() for identifier in card_identifiers.split(',')]

    cards_info = []
    for card_identifier in card_identifiers:
        card_found = False

        for card in available_cards:
            if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
                if any(card_identifier == search[0].card_number for search in user.searches):
                    await interaction.response.send_message("Tu recherches déjà la carte " + card_identifier)
                    card_found = True
                    break

                user.searches.append((card, []))
                cards_info.append(card)
                card_found = True

        if not card_found:
            await interaction.response.send_message(f"La carte spécifiée '{card_identifier}' n'existe pas.")

    if cards_info:
        embed = discord.Embed(title="Cartes recherchées", color=discord.Color.blue())
        for card in cards_info:
            embed.add_field(name=card.name, value=card.rarity, inline=False)
            #embed.set_image(url=card.image_url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande pour rechercher une carte spécifique en échange d'autres cartes spécifiées
@tree.command(guild=discord.Object(id=1122893178278785175), name='search_card_for_trade', description='Permet de rechercher une carte en échange d\'autres cartes spécifiées')
async def search_card_for_trade(interaction: discord.Interaction, card_to_search: str, trade_all_cards: bool, trade_cards: str):
    user = users.get(interaction.user.id)
    if user is None:
        user = User(interaction.user.name)
        users[interaction.user.id] = user

    card_to_search = card_to_search.strip()
    trade_cards = [card.strip() for card in trade_cards.split(',')]

    main_card = None
    trade_cards_list = []

    for card in available_cards:
        if card.card_number == card_to_search or (card.name + " " + card.rarity) == card_to_search:
            main_card = card
            break

    if main_card is None:
        await interaction.response.send_message(f"La carte spécifiée '{card_to_search}' n'existe pas.")
        return

    for trade_card in trade_cards:
        for card in available_cards:
            if card.card_number == trade_card or (card.name + " " + card.rarity) == trade_card:
                trade_cards_list.append(card)
                break

    if not trade_cards_list:
        await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.")
        return

    user.searches.append((main_card, trade_cards_list))

    embed = discord.Embed(title="Recherche de carte en échange", color=discord.Color.blue())
    embed.add_field(name="Carte recherchée", value=main_card.name, inline=False)

    if trade_all_cards:
        trade_description = "\n".join([card.name for card in trade_cards_list])
    else:
        trade_description = "\n".join([card.name for card in trade_cards_list])

    embed.add_field(name="Cartes proposées en échange", value=trade_description, inline=False)

    if trade_all_cards:
        embed.add_field(name="Proposition", value="Toutes les cartes affichées sont proposées en échange.", inline=False)
    else:
        embed.add_field(name="Proposition", value="Une carte parmi les cartes affichées est proposée en échange.", inline=False)

    await interaction.response.send_message(embed=embed)

# Commande pour proposer des cartes en échange
@tree.command(guild=discord.Object(id=1122893178278785175), name='trade_cards', description='Permet de signaler que vous avez une ou des cartes à échanger')
async def trade_cards(interaction: discord.Interaction, trade_cards: str):
    user = users.get(interaction.user.id)
    if user is None:
        user = User(interaction.user.name)
        users[interaction.user.id] = user

    trade_cards_list = [card.strip() for card in trade_cards.split(',')]

    user.trades.extend(trade_cards_list)
    valid_trade_cards = []
    for card_identifier in trade_cards_list:
        card_info = next((card for card in available_cards if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier), None)
        if card_info:
            valid_trade_cards.append(card_info)

    if not valid_trade_cards:
        await interaction.response.send_message("Veuillez spécifier une ou plusieurs cartes valides à échanger.")
        return

    embed = discord.Embed(title="Cartes proposées en échange", description="Voici les cartes que vous proposez en échange :", color=discord.Color.blue())
    for card in valid_trade_cards:
        embed.add_field(name=card.name, value=card.rarity, inline=False)
    await interaction.response.send_message(f"{interaction.user.mention} propose en échange :", embed=embed)

# Commande pour afficher les échanges en cours
@tree.command(guild=discord.Object(id=1122893178278785175), name='show_trades', description='Affiche les propositions de cartes en cours')
async def show_trades(interaction: discord.Interaction, cards: str = ""):
    cards = [card.strip() for card in cards.split(",")]

    if cards:
        # Cas où des cartes sont spécifiées
        trades = []
        for user in users.values():
            for trade in user.trades:
                card_info = next((card for card in available_cards if card.card_number == trade or card.name.lower() in trade.lower()), None)
                if card_info and any(card.lower() == trade.lower() or card.lower() in card_info.name.lower() or card.lower() in card_info.rarity.lower() for card in cards):
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
                trade_list = []
                for trade in user.trades:
                    card_info = next((card for card in available_cards if card.card_number == trade), None)
                    if card_info:
                        trade_list.append(f"{card_info.name} ({card_info.rarity})")
                if trade_list:
                    trades.append(f"{user.username} propose : {', '.join(trade_list)}")

        if trades:
            embed = discord.Embed(title="Liste de tous les échanges en cours", color=discord.Color.blue()) ## PROBLEME ICI: TITRE DE EMBED = "Échanges concernant les cartes spécifiées" MEME SI AUCUNE CARTE SPECIFIEE
            embed.description = "\n".join(trades)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Il n'y a pas d'échanges en cours.", ephemeral=True)

# Commande pour réinitialiser les recherches et échanges de l'utilisateur
@tree.command(guild=discord.Object(id=1122893178278785175), name='reset', description='Réinitialiser les recherches et échanges de l\'utilisateur')
async def reset(interaction: discord.Interaction):
    user = users.get(interaction.user.id)
    if user is None or (not user.searches and not user.trades):
        await interaction.response.send_message("Vous n'avez pas encore d'informations d'utilisateur enregistrées.", ephemeral=True)
        return

    user.reset()
    await interaction.response.send_message("Vos recherches et échanges ont été réinitialisés avec succès.", ephemeral=True)

# Commande pour supprimer une ou plusieurs cartes spécifiques des recherches/échanges de l'utilisateur
## ATTENTION PROBLEME: LE MESSAGE DE REPONSE NE RENVOI PAS LE NOM DES CARTES MAIS SEULEUMENT LEUR ID
@tree.command(guild=discord.Object(id=1122893178278785175), name='remove_card', description='Supprime une ou plusieurs cartes spécifiques des recherches/échanges de l\'utilisateur')
async def remove_card(interaction: discord.Interaction, card_identifiers: str):
    user = users.get(interaction.user.id)
    if user is None:
        await interaction.response.send_message("Vous n'avez pas encore d'informations d'utilisateur enregistrées.")
        return

    if not card_identifiers:
        await interaction.response.send_message("Veuillez spécifier les identifiants des cartes à supprimer.")
        return

    card_identifiers = [card.strip() for card in card_identifiers.split(",")]

    removed_cards = []
    for card_identifier in card_identifiers:
        # Supprimer les cartes correspondantes des recherches de l'utilisateur
        removed_searches = [search for search in user.searches if search[0].card_number == card_identifier or (search[0].name + " " + search[0].rarity) == card_identifier]
        for search in removed_searches:
            user.searches.remove(search)
            removed_cards.append(search[0].name)

        # Supprimer les cartes correspondantes des échanges de l'utilisateur
        removed_trades = [trade for trade in user.trades if trade == card_identifier]
        for trade in removed_trades:
            user.trades.remove(trade)
            removed_cards.append(trade)

    if removed_cards:
        await interaction.response.send_message(f"Les cartes suivantes ont été supprimées : {', '.join(removed_cards)}", ephemeral=True)
    else:
        await interaction.response.send_message("Aucune carte correspondante n'a été trouvée dans vos recherches ou échanges.", ephemeral=True)

# Connecte le bot au serveur
client.run('MTEyMjg5MTU0OTk0NTExNDc3NA.GU0nXT.tvLNPo1oBWWtvcgtetjY7MWJVdWYx6x8d-d530')