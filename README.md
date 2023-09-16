# Projet-Banque-NSI

### Installation
- Pour pouvoir utiliser le logiciel de banque il vous faut ouvrir le fichier "BankApp.py" présent dans le dossier "Client Side" et l'executer.
- Si il y a une erreur c'est peut-être à cause du fait que vous ne possedez pas les librairies Tkinter et/ou Requests. Dans ce cas téléchargez le/les.

### Fonctionnement
#### Client Side
- Le côté client (Client Side) peut être distribuer pour toute personne souhaitant souscrire à la banque. Il est utiliser comme interface graphique pour permettre à un utilisateur de gérer son compte bancaire.
- L'interface créé est faite grâce à la librairie Tkinter. Les requêtes envoyés au serveur sont quand à elle faites avec la librairie Requests.

#### Server Side
- Le côté serveur (Server Side) est utilisé sur un ordinateur de la banque pour gérer les différents compte, requestes de façon sécurisé et disponible de partout.
- Cette partie du code doit donc authentifier un utilisateur, traiter sa requête et renvoyer les informations tirées de bases de données.
- L'authentification de l'utilisateur se fait par la création d'un compte, la connexion avec un identifiant et un mot de passe ou si le client s'est déjà connecté sur la plateforme sur cet ordinateur dans un délais de 7 jours au maximum, à l'aide d'un token de connexion.
- Le traitement des requêtes se fait dans le fichier RequestManager.py. Pour ce faire on identifie la requête envoyé, on la traite en fonction et en faisant des vérifications et on renvoie des informations au client.
- La gestion des bases de données se fait dans le fichier DataManager.py. Ce fichier contenant plus ou moins qu'une classe, permet de gérer beaucoup plus facilement et rapidement les bases de données.

### Bug et autre problèmes
- Cela peut être problématique mais il n'y a pas de message d'erreur
- Aussi les variables sont très sensible, le système est sécurisé mais peut faire beaucoup d'erreur.
