# Importation des modules nécessaires
from fastapi import FastAPI       # FastAPI pour créer une application API
from dotenv import dotenv_values   # dotenv pour charger les configurations stockées dans le fichier .env
from pymongo import MongoClient    # MongoClient de PyMongo pour se connecter à une base de données MongoDB

# Charger les configurations depuis le fichier .env
config = dotenv_values(".env")

# Initialiser une instance FastAPI
app = FastAPI()

# Cette fonction se connecte à la base de données MongoDB au démarrage de l'application
@app.on_event("startup")
def startup_db_client():
    # Crée un client MongoDB en utilisant l'URI spécifié dans le fichier .env
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    
    # Sélectionne la base de données indiquée dans la configuration (.env) pour la rendre accessible dans l'application
    app.database = app.mongodb_client[config["DB_NAME"]]
    
    # Imprime un message dans la console pour confirmer que la connexion a réussi
    print("Connected to the MongoDB database!")

# Cette fonction ferme la connexion à MongoDB lorsque l'application est arrêtée
@app.on_event("shutdown")
def shutdown_db_client():
    # Ferme la connexion MongoDB proprement lors de l'arrêt de l'application
    app.mongodb_client.close()

# Route de test (commentée pour l'instant)
# @app.get("/")
# async def root():
#     # Renvoie un message JSON pour vérifier que l'application fonctionne
#     return {"message": "Welcome to the Pymongo tutorial!"}
