
# Trading Bot - Readme
Ce bot Discord permet aux utilisateurs de rechercher des cartes, de proposer des échanges et de consulter les échanges en cours.

## Commandes disponibles
Avant d'utiliser les commandes, assurez-vous que le bot est prêt en affichant le message "Bot is ready!".

### /show_available_cards
Affiche la liste des cartes disponibles.

Utilisation :
```
/show_available_cards
```

### /show_selected_cards
Affiche une ou plusieurs cartes spécifiées par leur identifiant ou leur nom + rareté.

Utilisation :
```
/show_selected_cards <id_carte1> <id_carte2> ...
```

### /search_card
Recherche une carte spécifiée par son identifiant ou son nom + rareté et l'ajoute à la liste de recherches de l'utilisateur.

Utilisation :
```
/search_card <id_carte>
```

### /search_card_for_trade
Recherche une carte spécifiée par son identifiant ou son nom + rareté et l'ajoute à la liste de recherches de l'utilisateur en spécifiant les cartes proposées en échange.

Utilisation :
```
/search_card_for_trade <id_carte> <id_carte1> <id_carte2> ...
```

### /trade_cards
Ajoute les cartes spécifiées à la liste d'échanges de l'utilisateur.

Utilisation :
```
/trade_cards <id_carte1> <id_carte2> ...
```

### /show_trades
Affiche les échanges en cours pour les cartes spécifiées ou tous les échanges en cours si aucune carte n'est spécifiée.

Utilisation :
```
/show_trades
```
ou
```
/show_trades <id_carte1> <id_carte2> ...
```

## Configuration du bot
Avant d'exécuter le bot, assurez-vous d'avoir configuré le jeton d'authentification. Vous devez fournir un jeton valide pour que le bot puisse fonctionner correctement.

Pour configurer le jeton d'authentification, modifiez la ligne suivante dans le script :

bot.run('VOTRE_JETON')
Remplacez VOTRE_JETON par le jeton d'authentification de votre bot Discord.

## Remarque
Ce README fournit une brève description des commandes disponibles et de leur utilisation. Vous pouvez personnaliser davantage le README en ajoutant des informations supplémentaires sur la configuration, les dépendances, etc., en fonction des besoins de votre projet.

N'oubliez pas de fournir des instructions claires et concises pour que les utilisateurs puissent utiliser le bot correctement.

C'est tout ! Maintenant, vous pouvez utiliser ce README comme guide pour aider les utilisateurs à comprendre et à utiliser votre bot Discord.

