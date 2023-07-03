#classes.py

class Card:
    def __init__(self, card_number, name, rarity, image_url):
        self.card_number = card_number
        self.name = name
        self.rarity = rarity
        self.image_url = image_url


    def to_dict(self):
        return {
            "card_number": self.card_number,
            "name": self.name,
            "rarity": self.rarity,
            "image_url": self.image_url
        }
    
    def lower(self):
        return str(self).lower()

    def __str__(self):
        return self.name

class User:
    def __init__(self, username):
        self.username = username
        self.searches = []  # Liste des recherches en cours de l'utilisateur (contenant des objets Card)
        self.trades = []  # Liste des échanges en cours de l'utilisateur (contenant des objets Card)
        self.score = 0  # Score de l'utilisateur
    
    def reset(self):
        self.searches = []
        self.trades = []
        self.score = 0
    
    def to_dict(self):
        return {
            "username": self.username,
            "searches": [card.to_dict() for card in self.searches],
            "trades": [card.to_dict() for card in self.trades],
            "score": self.score,
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(data['username'])
        user.searches = [Card(card_info['card_number'], card_info['name'], card_info['rarity'], card_info['image_url']) for card_info in data['searches']]
        user.trades = [Card(card_info['card_number'], card_info['name'], card_info['rarity'], card_info['image_url']) for card_info in data['trades']]
        user.score = data['score']
        return user