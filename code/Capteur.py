import sqlite3
import random
import time
import httpx
from datetime import datetime

# Configuration de la base de données
DB_PATH = "logement.db"

# Configuration de l'API météo
API_KEY = "19a0ca2291c83708d91e302ee4d74235"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = "Paris"

# Fonction pour récupérer la température extérieure
def get_outdoor_temperature():
    try:
        response = httpx.get(BASE_URL, params={"q": CITY, "appid": API_KEY, "units": "metric"})
        response.raise_for_status()
        data = response.json()
        return data["main"]["temp"]  # Température extérieure
    except httpx.RequestError as e:
        print(f"❌ Erreur lors de la récupération de la météo : {e}")
        return None

# Fonction pour insérer des mesures simulées dans la base de données
def insert_sensor_data(sensor_id, value):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO mesure (capteur_actionneur_id, valeur, date_insertion)
                VALUES (?, ?, ?)
            """, (sensor_id, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL lors de l'insertion des mesures : {e}")

# Fonction pour insérer une action dans la base de données
def insert_action(sensor_id, action_type):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO action (capteur_id, type_action, date_insertion)
                VALUES (?, ?, ?)
            """, (sensor_id, action_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL lors de l'insertion de l'action : {e}")

# Fonction pour gérer les actions en fonction des mesures
def handle_actions(sensor, value):
    if sensor["type"] == "température":
        if value > 25:  # Seuil arbitraire de 25°C
            action_type = "Allumer LED"
            print(f"⚠️ Température élevée détectée par le capteur {sensor['id']} : {value}°C. Action : {action_type}.")
            insert_action(sensor["id"], action_type)
        else:
            action_type = "Éteindre LED"
            print(f"✅ Température normale détectée par le capteur {sensor['id']} : {value}°C. Action : {action_type}.")
            insert_action(sensor["id"], action_type)
    elif sensor["type"] == "humidité" and value < 30:  # Seuil pour l'humidité
        action_type = "Envoyer alerte : Humidité basse"
        print(f"⚠️ Humidité basse détectée par le capteur {sensor['id']} : {value}%. Action : {action_type}.")
        insert_action(sensor["id"], action_type)
    else:
        print(f"ℹ️ Aucune action nécessaire pour le capteur {sensor['id']} ({sensor['type']}).")

# Fonction pour simuler les capteurs
def simulate_sensors():
    while True:
        # Récupérer la température extérieure
        outdoor_temp = get_outdoor_temperature()
        if outdoor_temp is None:
            print("🔄 Réessai dans 10 secondes...")
            time.sleep(10)
            continue

        print(f"🌡️ Température extérieure : {outdoor_temp}°C")

        # Simuler des capteurs
        sensors = [
            {"id": 1, "type": "température", "variation": 2},  # Simule un capteur de température
            {"id": 2, "type": "humidité", "variation": 5},    # Simule un capteur d'humidité
            {"id": 3, "type": "luminosité", "variation": 20}, # Simule un capteur de luminosité
        ]

        for sensor in sensors:
            if sensor["type"] == "température":
                # Simule une température proche de la température extérieure
                simulated_value = round(outdoor_temp + random.uniform(-sensor["variation"], sensor["variation"]), 2)
            else:
                # Génère une valeur aléatoire pour les autres capteurs
                simulated_value = round(random.uniform(20, 100), 2)
            
            print(f"📟 Capteur {sensor['id']} ({sensor['type']}) -> Valeur simulée : {simulated_value}")
            insert_sensor_data(sensor["id"], simulated_value)
            handle_actions(sensor, simulated_value)

        # Pause entre chaque simulation
        time.sleep(5)  # Simule une mise à jour toutes les 5 secondes

if __name__ == "__main__":
    simulate_sensors()
