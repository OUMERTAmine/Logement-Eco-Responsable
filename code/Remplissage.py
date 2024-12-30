import sqlite3
import random
from datetime import datetime

# Variables globales
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Connexion à la base de données
    with sqlite3.connect("logement.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Insertion d'un nouveau logement
        new_logement = {
            "adresse": "10 Avenue des Champs Élysées, Paris",
            "telephone": "0678945612",
            "ip": "10.0.0.1",
            "date_insertion": CURRENT_TIMESTAMP
        }
        c.execute("""
            INSERT INTO logement (adresse, telephone, ip, date_insertion)
            VALUES (:adresse, :telephone, :ip, :date_insertion)
        """, new_logement)
        new_logement_id = c.lastrowid  # ID du nouveau logement inséré

        # Insertion de nouvelles pièces pour ce logement
        new_pieces = [
            {"nom": "bureau", "coordonnees": "x=1 y=2 z=3"},
            {"nom": "terrasse", "coordonnees": "x=2 y=1 z=3"},
            {"nom": "garage", "coordonnees": "x=0 y=0 z=1"},
            {"nom": "jardin", "coordonnees": "x=3 y=2 z=0"}
        ]
        for piece in new_pieces:
            piece_data = {
                "logement_id": new_logement_id,
                "nom": piece["nom"],
                "coordonnees": piece["coordonnees"]
            }
            c.execute("""
                INSERT INTO piece (logement_id, nom, coordonnees)
                VALUES (:logement_id, :nom, :coordonnees)
            """, piece_data)

        # Insertion de nouveaux types de capteurs/actionneurs
        new_types = [
            {"nom": "CO2", "unite": "ppm", "precision_capteur": 90},
            {"nom": "pression atmosphérique", "unite": "hPa", "precision_capteur": 100},
            {"nom": "bruit", "unite": "dB", "precision_capteur": 85},
            {"nom": "humidité du sol", "unite": "%", "precision_capteur": 95}
        ]
        for capteur_type in new_types:
            c.execute("""
                INSERT OR IGNORE INTO type_capteur_actionneur (nom, unite, precision_capteur)
                VALUES (:nom, :unite, :precision_capteur)
            """, capteur_type)

        # Insertion de capteurs/actionneurs pour les nouvelles pièces
        new_capteurs_actionneurs = [
            {"piece_id": 1, "type_id": 6, "reference": "CO2SensorX", "port": "5001"},
            {"piece_id": 2, "type_id": 7, "reference": "PressureSensorY", "port": "5002"},
            {"piece_id": 3, "type_id": 8, "reference": "NoiseDetectorZ", "port": "5003"},
            {"piece_id": 4, "type_id": 9, "reference": "SoilMoisture", "port": "5004"}
        ]
        for capteur in new_capteurs_actionneurs:
            c.execute("""
                INSERT INTO capteur_actionneur (piece_id, type_id, reference, port, date_insertion)
                VALUES (:piece_id, :type_id, :reference, :port, :date_insertion)
            """, {**capteur, "date_insertion": CURRENT_TIMESTAMP})

        # Insertion de nouvelles mesures pour les capteurs/actionneurs
        new_mesures = [
            {"capteur_actionneur_id": 4, "valeur": random.uniform(300, 800)},  # CO2
            {"capteur_actionneur_id": 5, "valeur": random.uniform(950, 1050)},  # Pression
            {"capteur_actionneur_id": 6, "valeur": random.uniform(40, 90)},     # Bruit
            {"capteur_actionneur_id": 7, "valeur": random.uniform(10, 40)}      # Humidité du sol
        ]
        for mesure in new_mesures:
            c.execute("""
                INSERT INTO mesure (capteur_actionneur_id, valeur, date_insertion)
                VALUES (:capteur_actionneur_id, :valeur, :date_insertion)
            """, {**mesure, "date_insertion": CURRENT_TIMESTAMP})

        # Insertion de nouvelles factures pour le logement
        new_factures = [
            {"logement_id": new_logement_id, "type": "chauffage", "date": "2024-01-15", "montant": 100, "valeur_consomme": 400},
            {"logement_id": new_logement_id, "type": "internet", "date": "2024-02-10", "montant": 30, "valeur_consomme": 0},
            {"logement_id": new_logement_id, "type": "assainissement", "date": "2024-03-05", "montant": 20, "valeur_consomme": 50},
            {"logement_id": new_logement_id, "type": "maintenance", "date": "2024-04-01", "montant": 150, "valeur_consomme": 0}
        ]
        for facture in new_factures:
            c.execute("""
                INSERT INTO facture (logement_id, type, date, montant, valeur_consomme)
                VALUES (:logement_id, :type, :date, :montant, :valeur_consomme)
            """, facture)

        conn.commit()
        print("Nouveaux exemples de données insérés avec succès !")

except sqlite3.Error as e:
    print(f"Erreur lors de l'interaction avec la base de données : {e}")
