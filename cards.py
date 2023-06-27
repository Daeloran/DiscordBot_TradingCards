class Card:
    def __init__(self, card_number, name, rarity, image_url):
        self.card_number = card_number
        self.name = name
        self.rarity = rarity
        self.image_url = image_url

class User:
    def __init__(self, username):
        self.username = username
        self.searches = []  # Liste des recherches en cours de l'utilisateur (contenant des tuples (numéro de carte, nom de carte, rareté))
        self.trades = []  # Liste des échanges en cours de l'utilisateur (contenant des tuples (numéro de carte, nom de carte, rareté))
    def reset(self):
        self.searches = []
        self.trades = []

available_cards = [
    Card("LDD-F003", "Magicien Sombre", "Ultra Rare", "http://www.ultrajeux.com/images/yugioh/scan/maxi/fr/ldd-f/ldd-f003.jpg"),
    Card("LDD-F101", "Exodia l'Interdit", "Ultra Rare", "http://www.ultrajeux.com/images/yugioh/scan/maxi/fr/ldd-f/ldd-f101.jpg"),
    Card("MRD-F001", "Lutin Sauvage", "Commune", "http://www.ultrajeux.com/images/yugioh/scan/maxi/fr/mrd/mrd-f001.jpg"),
    # Ajoute d'autres cartes ici
]
