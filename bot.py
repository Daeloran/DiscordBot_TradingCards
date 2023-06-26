import discord
from discord.ext import commands

from cards import Card, available_cards, User


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/',intents=intents)


#IDEES : commande pour afficher une carte en particulier

@bot.event
async def on_ready():
    print('Bot is ready!')

users = {}  # Dictionnaire pour stocker les informations des utilisateurs
cards_available = {}  # Dictionnaire pour stocker les cartes disponibles


# Commande pour afficher les cartes existantes
@bot.command()
async def show_available_cards(ctx):
    for card in available_cards:
        embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
        embed.set_image(url=card.image_url)
        await ctx.send(embed=embed)

@bot.command()
async def show_selected_cards(ctx, *card_identifiers):
    if not card_identifiers:
        await ctx.send("Veuillez spécifier au moins une carte.")
        return

    cards_info = []
    for card_identifier in card_identifiers:
        card_info = get_card_information(card_identifier)
        if card_info:
            cards_info.append(card_info)

    if cards_info:
        for card in cards_info:
            embed = discord.Embed(title=card.name, description=card.rarity, color=discord.Color.blue())
            embed.set_image(url=card.image_url)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Aucune carte trouvée.")


# Fonction pour obtenir les informations de la carte en fonction de son identifiant
def get_card_information(card_identifier):
    for card in available_cards:
        if card.card_number == card_identifier or (card.name + " " + card.rarity) == card_identifier:
            return card
    return None

@bot.command()
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

@bot.command()
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
@bot.command()
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

@bot.command()
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


bot.run('MTEyMjg5MTU0OTk0NTExNDc3NA.GU0nXT.tvLNPo1oBWWtvcgtetjY7MWJVdWYx6x8d-d530')
