-- Activer les contraintes de clés étrangères (SQLite uniquement)
PRAGMA foreign_keys = ON;

-- Supprime les tables si elles existent
DROP TABLE IF EXISTS action;
DROP TABLE IF EXISTS mesure;
DROP TABLE IF EXISTS facture;
DROP TABLE IF EXISTS capteur_actionneur;
DROP TABLE IF EXISTS type_capteur_actionneur;
DROP TABLE IF EXISTS piece;
DROP TABLE IF EXISTS logement;
DROP TABLE IF EXISTS typecapteuractionneur;
DROP TABLE IF EXISTS capteuractionneur ;
-- Création des tables

-- Table logement
CREATE TABLE logement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Identifiant unique du logement
    adresse TEXT NOT NULL,                     -- Adresse du logement
    telephone TEXT NOT NULL,                   -- Téléphone du logement
    ip TEXT NOT NULL UNIQUE,                   -- Adresse IP unique du logement
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Date d'insertion
);

-- Table piece
CREATE TABLE piece (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Identifiant unique de la pièce
    logement_id INTEGER NOT NULL,             -- Identifiant du logement
    nom TEXT NOT NULL,                        -- Nom de la pièce
    coordonnees TEXT,                         -- Coordonnées de la pièce (optionnel)
    FOREIGN KEY (logement_id) REFERENCES logement(id)
);

-- Table type_capteur_actionneur
CREATE TABLE type_capteur_actionneur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Identifiant unique du type de capteur/actionneur
    nom TEXT NOT NULL UNIQUE,                -- Nom du type de capteur/actionneur
    unite TEXT NOT NULL,                     -- Unité de mesure
    precision_capteur REAL                   -- Précision du capteur
);

-- Table capteur_actionneur
CREATE TABLE capteur_actionneur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    -- Identifiant unique du capteur/actionneur
    piece_id INTEGER NOT NULL,              -- Référence vers la pièce
    type_id INTEGER NOT NULL,               -- Référence vers le type de capteur/actionneur
    reference TEXT NOT NULL,                -- Référence commerciale du capteur/actionneur
    port TEXT NOT NULL,                     -- Port de communication
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date d'insertion
    FOREIGN KEY (piece_id) REFERENCES piece(id),
    FOREIGN KEY (type_id) REFERENCES type_capteur_actionneur(id)
);

-- Table mesure
CREATE TABLE mesure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identifiant unique de la mesure
    capteur_actionneur_id INTEGER NOT NULL, -- Référence vers le capteur/actionneur
    valeur REAL NOT NULL,                   -- Valeur mesurée
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date d'insertion de la mesure
    FOREIGN KEY (capteur_actionneur_id) REFERENCES capteur_actionneur(id)
);
CREATE INDEX idx_mesure_capteur ON mesure(capteur_actionneur_id);  -- Index pour optimiser les requêtes

-- Table facture
CREATE TABLE facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identifiant unique de la facture
    logement_id INTEGER NOT NULL,          -- Référence vers le logement
    type TEXT NOT NULL,                    -- Type de facture (eau, électricité, etc.)
    date DATE NOT NULL,                    -- Date de la facture
    montant REAL NOT NULL,                 -- Montant de la facture
    valeur_consomme REAL,                  -- Valeur consommée
    FOREIGN KEY (logement_id) REFERENCES logement(id)
);

-- Table action
CREATE TABLE action (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique de l'action
    capteur_id INTEGER NOT NULL,           -- Référence vers le capteur/actionneur
    type_action TEXT NOT NULL,             -- Type d'action (ex : "Allumer LED")
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date de l'action
    FOREIGN KEY (capteur_id) REFERENCES capteur_actionneur(id)
);
CREATE INDEX idx_action_capteur ON action(capteur_id);  -- Index pour optimiser les requêtes

-- Insertion des données initiales

-- Ajouter un logement
INSERT INTO logement (adresse, telephone, ip, date_insertion)
VALUES
('5 rue jussieu paris', '0745718200', '192.168.123.132', '2024-11-08');

-- Ajouter des pièces
INSERT INTO piece (logement_id, nom, coordonnees)
VALUES
(1, 'cuisine', 'x=2 y=3 z=5'),
(1, 'chambre', 'x=2 y=4 z=5'),
(1, 'salon', 'x=3 y=3 z=5'),
(1, 'salle de bain', 'x=2 y=5 z=5');

-- Ajouter des types de capteurs/actionneurs
INSERT INTO type_capteur_actionneur (nom, unite, precision_capteur)
VALUES
('température', '°C', 95),
('humidité', '%', 97),
('luminosité', 'lumens / m2', 80),
('électricité', 'KWh', 99),
('Gaz', 'm^3', 99);

-- Ajouter des capteurs/actionneurs
INSERT INTO capteur_actionneur (piece_id, type_id, reference, port, date_insertion)
VALUES
(1, 1, 'DHT22', '1234', '2024-11-08'),
(3, 3, 'Ardu37', '4321', '2024-11-08'),
(1, 5, 'totale', '2254', '2024-11-08');

-- Ajouter des mesures
INSERT INTO mesure (capteur_actionneur_id, valeur, date_insertion)
VALUES
(1, 25, '2024-11-08'),
(1, 28, '2024-11-10'),
(2, 80, '2024-11-10'),
(2, 75, '2024-11-12'),
(3, 230845, '2024-11-12'),
(3, 239845, '2024-12-12');

-- Ajouter des factures
INSERT INTO facture (logement_id, type, date, montant, valeur_consomme)
VALUES
(1, 'eau', '2024-11-08', 50, 250),
(1, 'électricité', '2024-11-10', 200, 2587),
(1, 'gaz', '2024-11-10', 60, 120),
(1, 'électricité', '2024-12-12', 190, 2500);
