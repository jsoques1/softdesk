# Créez une API sécurisée RESTful en utilisant Django REST

## Objet

Se référer aux spécifications données sur la page https://openclassrooms.com/fr/paths/518/projects/838/assignment

## Installation

- cloner les sources avec 

    git clone https://github.com/jsoques1/softdesk

- se déplacer dans le sous répertoire de travail softdesk

    cd softdesk

- créer un environnement virtuel python, venv

    python -m venv venv

- activer un environnement virtuel python, venv

    venv\Scripts\activate.bat

- installer les paquets requis

    pip install -r requirements.txt

- exécuter la migration des modèles (non nécessaire si le fichier DB db.sqlite3 n'est pas supprimé, voir ci-dessous)

    python manage.py migrate

- lancer le serveur

    python manage.py runserver

- accéder à l'application SoftDesk serveur via le WEB à l'URL :

    http://127.0.0.1:8000/login/


Comme requis un exemple de travail du fichier DB db.sqlite3 est livré et permet de démarrer sans effectuer la migration des modèles. 
Si vous souhaitez débuter avec une base de donnée vierge, il vous suffit de supprimer le fichier db.sqlite3 ; 
l'application en créera un nouveau à la migration des modèles.

## Liste des utilisateurs 

| id   | username      | password       |
|------|---------------|----------------|
| 1    | admin         | p@ssword2022   |
| 2    | student       | p@ssword2022   |
| 3    | intern        | p@ssword2022   |
| 4    | tester        | p@ssword2022   |

L'utilisateur admin sera créé de préférence dans l'environnement virtuel avec la commande shell createsuperuser.

- python manage.py createsuperuser

Les autres utilisateurs seront créés avec l'endpoint signup.


## API documentation

Se référer à la page https://documenter.getpostman.com/view/20394225/UzQuPRTc
