Structure du projets : 

code/
│
├── Serveur.py
├── logement.db
├── Capteur.py
├──logementEcoResponsable.sql
├──Remplissage.py
├── templates/
│   ├── Interface_Web.html
│   ├── logement.html
│   ├── pieces.html
│   ├── capteurs.html
│   ├── mesures.html
│   ├── actions.html
│   ├── facture.html
    ├── meteo.htm
│
├── static/
│   
│   │   ├── Acceuil.css
│   │   ├── logement.css
│   │   ├── pieces.css
│   │   ├── meteo.css
│   │
│   ├── js/
│       ├── logement.js
│       ├── pieces.js
│       ├── capteur.js
│       ├── mesures.js
│       ├── actions.js
│       ├── factures.js
	 ├── meteo.js
│
└── README.text


Instructions pour exécuter le projet : Logement Éco-Responsable

1. installation les Dépendances nécessaires

- Python 
- FastAPI
- Uvicorn
- SQLModel
- SQLite
- Bootstrap (inclus dans le projet via un CDN)
- Chart.js (inclus via un CDN pour les graphiques)

2. Préparation initiale
Ouvrez un terminal 
3.Naviguez jusqu’au répertoire du projet : cd /chemin/vers/le/projet
4.Exécutez la commande suivante pour ouvrir SQLite : sqlite3 logement.db
5.Chargez le fichier SQL pour créer la structure de la base de données : .read logementEcoResponsable.sql
6.Remplissez la base de données avec des données initiales, Exécutez le fichier Python de remplissage des données:  python Remplissage.py
7.Ajoutez des mesures simulées depuis un ESP32 : Exécutez le fichier suivant pour insérer des mesures dans la base de données : python capteur.py
8.Configuration du serveur : Configurez les chemins pour les fichiers templates et static dans le fichier Serveur.py :
			     Ouvrez le fichier Serveur.py et modifiez les lignes suivantes : 
						 templates = Jinja2Templates(directory="C:/chemin/vers/templates")    CHANGER LE CHEMIN VERS LE REPARTOIRE TEMPLATES 
						 app.mount("/static", StaticFiles(directory="C:/chemin/vers/static"), name="static")   CHANGER LE CHEMIN VERS LE REPARTOIRE Static

Démarrez le serveur FastAPI :  python Serveur.py

9. Tester le serveur API
Ouvrez votre navigateur et accédez à : http://127.0.0.1:8000/docs
Testez les routes du serveur :
Effectuez des requêtes GET sur toutes les routes disponibles pour valider leur bon fonctionnement et pour mis a jour les données des interface web crée

10.Tester l’interface web
Lancer l'interface web :
Accédez au fichier Interface_Web.html dans le dossier templates et Naviguez entre les pages.














