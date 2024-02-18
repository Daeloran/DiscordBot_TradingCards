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
        self.evaluations = []  # Liste des évaluations de l'utilisateur

    def reset(self):
        self.searches = []
        self.trades = []
        self.score = 0
        #self.evaluations = []

    def to_dict(self):
        return {
            "username": self.username,
            "searches": [card.to_dict() for card in self.searches],
            "trades": [card.to_dict() for card in self.trades],
            "score": self.score,
            "evaluations": [evaluation.to_dict() for evaluation in self.evaluations],
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['username'])
        user.searches = [Card.from_dict(card_info) for card_info in data['searches']]
        user.trades = [Card.from_dict(card_info) for card_info in data['trades']]
        user.score = data['score']
        user.evaluations = [Evaluation.from_dict(evaluation_info) for evaluation_info in data.get('evaluations', [])]
        return user

    def add_evaluation(self, evaluation):
        self.evaluations.append(evaluation)

    def remove_evaluation(self, evaluation):
        self.evaluations.remove(evaluation)

    
class Evaluation:
    def __init__(self, evaluator_username, rating, comment=None, cards_sent=None):
        self.evaluator_username = evaluator_username
        self.rating = rating
        self.comment = comment
        self.cards_sent = cards_sent if cards_sent is not None else []

    def to_dict(self):
        return {
            "evaluator_username": self.evaluator_username,
            "rating": self.rating,
            "comment": self.comment,
            "cards_sent": self.cards_sent,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["evaluator_username"],
            data["rating"],
            comment=data.get("comment"),
            cards_sent=data.get("cards_sent"),
        )
