import discord
from discord.ext import commands
from discord import app_commands
from cards import Card, available_cards, User


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/',intents=intents)
"""
@bot.event
async def on_ready():
    print('Bot is ready!')
"""

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=1122893178278785175)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

users = {}  # Dictionnaire pour stocker les informations des utilisateurs
cards_available = {}  # Dictionnaire pour stocker les cartes disponibles

@tree.command(guild = discord.Object(id=1122893178278785175), name = 'help_trade', description='Liste des commandes disponibles')
#async def help_trade(ctx):
async def slash2(interaction: discord.Interaction):
    embed = discord.Embed(title="Liste des commandes", description="Voici une liste des commandes que vous pouvez utiliser :", color=discord.Color.blue())
    embed.add_field(name="/show_available_cards", value="Afficher toutes les cartes disponibles.", inline=False)
    embed.add_field(name="/show_selected_cards [card_identifiers]", value="Afficher les cartes spécifiées par leurs identifiants.", inline=False)
    embed.add_field(name="/search_card [card_identifier]", value="Rechercher une carte spécifique par son identifiant.", inline=False)
    embed.add_field(name="/search_card_for_trade [card_identifier] [trade_cards]", value="Rechercher une carte à échanger contre d'autres cartes.", inline=False)
    embed.add_field(name="/trade_cards [trade_cards]", value="Proposer des cartes en échange.", inline=False)
    embed.add_field(name="/show_trades [cards]", value="Afficher les échanges en cours pour des cartes spécifiées.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(guild = discord.Object(id=1122893178278785175), name = 'show_available_cards', description='Liste l\'ensemble des cartes')
async def slash2(interaction: discord.Interaction):
    # Répond à l'interaction avec le premier message
    first_card = available_cards[0]
    embed = discord.Embed(title=first_card.name, description=first_card.rarity, color=discord.Color.blue())
    embed.set_image(url=first_card.image_url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # Envoie des messages de suivi avec les cartes restantes
    for card in available_cards[1:]:
        embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
        embed.set_image(url=card.image_url)
        await interaction.followup.send(embed=embed, ephemeral=True)

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

@tree.command(guild=discord.Object(id=1122893178278785175), name='search_card', description='Permet de signaler que vous recherchez une carte')
async def search_card(interaction: discord.Interaction, card_identifiers: str):
    user = users.get(interaction.user.id)
    if user is None:
        user = User(interaction.user.name)
        users[interaction.user.id] = user

    card_identifiers = [identifier.strip() for identifier in card_identifiers.split(',')]

    for card_identifier in card_identifiers:
        for card in available_cards:
            if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
                if any(card_identifier == search[0].card_number for search in user.searches):
                    await interaction.response.send_message("Tu recherches déjà la carte " + card_identifier)
                    continue

                user.searches.append((card, []))
                embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
                embed.set_image(url=card.image_url)
                await interaction.response.send_message(f"{interaction.user.mention} recherche la carte '{card.name}' ({card.rarity}).", embed=embed)

                # Envoi de messages supplémentaires avec les autres cartes recherchées
                additional_messages = []
                for search_card, search_messages in user.searches:
                    if search_card != card:  # Exclure la carte actuelle
                        additional_messages.append(f"Carte recherchée : {search_card.name} ({search_card.rarity})")
                        additional_messages.extend(search_messages)

                if additional_messages:
                    additional_messages_text = "\n".join(additional_messages)
                    await interaction.followup.send(additional_messages_text)

                break
        else:
            await interaction.response.send_message("La carte spécifiée n'existe pas.")



"""
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'search_card', description='Permet de signaler que vous rechercher une carte')
async def search_card(ctx, card_identifier):
    user = users.get(ctx.author.id)
    if user is None:
        user = User(ctx.author.name)
        users[ctx.author.id] = user

    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            if any(card_identifier == search[0].card_number for search in user.searches):
                await ctx.send("Tu recherches déjà cette carte.")
                return

            user.searches.append((card, []))
            embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
            embed.set_image(url=card.image_url)
            await ctx.send(f"{ctx.author.mention} recherche la carte '{card.name}' ({card.rarity}).", embed=embed)
            return

    await ctx.send("La carte spécifiée n'existe pas.")

@tree.command(guild = discord.Object(id=1122893178278785175), name = 'search_card_for_trade', description='Permet de signaler que vous recherchez une cartes en échanges d\'une carte particulière')
async def search_card_for_trade(ctx, card_identifier, *trade_cards):
    user = users.get(ctx.author.id)
    if user is None:
        user = User(ctx.author.name)
        users[ctx.author.id] = user

    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            if any(card_identifier == search[0].card_number for search in user.searches):
                await ctx.send("Tu recherches déjà cette carte.")
                return

            user.searches.append((card, list(trade_cards)))
            embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
            embed.set_image(url=card.image_url)

            trade_card_info = []
            for trade_card_identifier in trade_cards:
                trade_card = next((c for c in available_cards if c.card_number == trade_card_identifier or (c.name + " " + c.rarity) == trade_card_identifier), None)
                if trade_card:
                    trade_card_info.append(f"{trade_card.name} ({trade_card.rarity})")
            trade_card_text = ", ".join(trade_card_info)

            await ctx.send(f"{ctx.author.mention} recherche la carte '{card.name}' ({card.rarity}) en échange de {trade_card_text}.", embed=embed)
            return

    await ctx.send("La carte spécifiée n'existe pas.")


# 
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'trade_cards', description='Permet de signaler que vous avez une ou des cartes à échanger')
async def trade_cards(ctx, *trade_cards):
    user = users.get(ctx.author.id)
    if user is None:
        user = User(ctx.author.name)
        users[ctx.author.id] = user

    trade_cards = list(trade_cards)
    user.trades.extend(trade_cards)
    valid_trade_cards = []
    for card_identifier in trade_cards:
        card_info = next((card for card in available_cards if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier), None)
        if card_info:
            valid_trade_cards.append(card_info)

    embed = discord.Embed(title="Cartes proposées en échange", description="Voici les cartes que vous proposez en échange :", color=discord.Color.blue())
    for card in valid_trade_cards:
        embed.add_field(name=card.name, value=card.rarity, inline=False)
    await ctx.send(f"{ctx.author.mention} propose en échange :", embed=embed)

@tree.command(guild = discord.Object(id=1122893178278785175), name = 'show_trades', description='Affiche les propositions de cartes en cours')
async def show_trades(ctx, *cards):
    if cards:
        # Cas où des cartes sont spécifiées
        trades = []
        for user in users.values():
            for trade in user.trades:
                card_info = next((card for card in available_cards if card.card_number == trade or (card.name.lower() in trade.lower())), None)
                if card_info and any(card.lower() == trade.lower() or card.lower() in card_info.name.lower() or card.lower() in card_info.rarity.lower() for card in cards):
                    trades.append(f"{user.username} propose : {card_info.name} ({card_info.rarity})")

        if trades:
            await ctx.send("Voici les échanges concernant les cartes spécifiées :")
            await ctx.send("\n".join(trades))
        else:
            await ctx.send("Il n'y a pas d'échanges en cours pour les cartes spécifiées.")
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
            await ctx.send("Voici la liste de tous les échanges en cours :")
            await ctx.send("\n".join(trades))
        else:
            await ctx.send("Il n'y a pas d'échanges en cours.")

# Commande "reset" pour réinitialiser les recherches et échanges de l'utilisateur
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'reset', description='Réinitialiser les recherches et échanges de l\'utilisateur')
async def reset(ctx):
    user = users.get(ctx.author.id)
    if user is None:
        await ctx.send("Vous n'avez pas encore d'informations d'utilisateur enregistrées.")
        return

    user.reset()
    await ctx.send("Vos recherches et échanges ont été réinitialisés avec succès.")

# Commande "remove_card" pour supprimer une ou plusieurs cartes spécifiques des recherches/échanges de l'utilisateur
# ATTENTION: SEUL UNE CARTE EST MENTIONNEE DANS LE TEXTE DE RETOUR SI L'ON MET PLUSIEURS CARTES DANS LA COMMANDE
@tree.command(guild = discord.Object(id=1122893178278785175), name = 'remove_card', description='Supprime une ou plusieurs cartes spécifiques des recherches/échanges de l\'utilisateur')
async def remove_card(ctx, *card_identifiers):
    user = users.get(ctx.author.id)
    if user is None:
        await ctx.send("Vous n'avez pas encore d'informations d'utilisateur enregistrées.")
        return

    if not card_identifiers:
        await ctx.send("Veuillez spécifier les identifiants des cartes à supprimer.")
        return

    removed_cards = []
    for card_identifier in card_identifiers:
        # Supprimer les cartes correspondantes des recherches de l'utilisateur
        removed_searches = [search for search in user.searches if search[0].card_number == card_identifier or (search[0].name + " " + search[0].rarity) == card_identifier]
        user.searches = [search for search in user.searches if search not in removed_searches]

        # Supprimer les cartes correspondantes des échanges de l'utilisateur
        removed_trades = [trade for trade in user.trades if trade == card_identifier or any((card.card_number == trade or (card.name + " " + card.rarity) == trade) for card in available_cards)]
        user.trades = [trade for trade in user.trades if trade not in removed_trades]

        for search in removed_searches:
            removed_cards.append(search[0].name)

        card_info = next((card for card in available_cards if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier), None)
        if card_info and card_info.name not in removed_cards:
            removed_cards.append(card_info.name)

    if removed_cards:
        await ctx.send(f"Les cartes suivantes ont été supprimées : {', '.join(removed_cards)}")
    else:
        await ctx.send("Aucune carte correspondante n'a été trouvée dans vos recherches ou échanges.")
"""

#bot.run('MTEyMjg5MTU0OTk0NTExNDc3NA.GU0nXT.tvLNPo1oBWWtvcgtetjY7MWJVdWYx6x8d-d530')
client.run('MTEyMjg5MTU0OTk0NTExNDc3NA.GU0nXT.tvLNPo1oBWWtvcgtetjY7MWJVdWYx6x8d-d530')