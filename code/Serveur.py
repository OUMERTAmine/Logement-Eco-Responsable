from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List
from datetime import datetime
import httpx
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Serveur IoT pour Logement Éco-Responsable",
    description="Ce serveur gère les logements, capteurs, mesures, et actions avec des fonctionnalités d'automatisation.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez "*" par une liste de domaines spécifiques pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/static"), name="static")

# Configuration de la base de données
sqlite_file_name = "logement.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Configuration de l'API météo
API_KEY = "19a0ca2291c83708d91e302ee4d74235"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Fonction pour créer les tables SQL
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Gestion de session SQL
def get_session():
    with Session(engine) as session:
        yield session

# Fonction pour récupérer la température extérieure
@app.get("/meteo-5jours", status_code=status.HTTP_200_OK, tags=["Météo"])
def get_meteo_5jours(city: str = "Paris"):
    try:
        # Effectuer une requête à l'API météo pour les prévisions sur 5 jours
        response = httpx.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric"}
        )
        response.raise_for_status()
        data = response.json()

        # Extraire les informations météo par tranche de 3 heures
        previsions = []
        for item in data["list"]:
            previsions.append({
                "date_heure": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "humidite": item["main"]["humidity"],
                "pression": item["main"]["pressure"],
                "description": item["weather"][0]["description"],
                "vent_vitesse": item["wind"]["speed"],
                "vent_direction": item["wind"].get("deg", "Non spécifié"),
                "coordonnees": data["city"]["coord"]
            })

        return {
            "ville": data["city"]["name"],
            "coordonnees": data["city"]["coord"],
            "previsions": previsions
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à l'API météo : {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Erreur de l'API météo : {e}")

# Définition des modèles SQLModel
class Logement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    adresse: str
    telephone: str
    ip: str
    date_insertion: str | None = None

class Piece(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    logement_id: int = Field(foreign_key="logement.id")
    nom: str
    coordonnees: str

class type_capteur_actionneur(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    nom: str
    unite: str
    precision_capteur: float

class capteur_actionneur(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    piece_id: int = Field(foreign_key="piece.id")
    type_id: int = Field(foreign_key="typecapteuractionneur.id")
    reference: str
    port: str
    date_insertion: str | None = None

class Mesure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    capteur_actionneur_id: int = Field(foreign_key="capteur_actionneur.id")
    valeur: float
    date_insertion: str | None = None

class Facture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    logement_id: int = Field(foreign_key="logement.id")
    type: str
    date: str
    montant: float
    valeur_consomme: float

class Action(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    capteur_id: int = Field(foreign_key="capteur_actionneur.id")
    type_action: str
    date_insertion: str | None = None

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Route pour afficher la page d'accueil
@app.get("/", response_class=HTMLResponse, tags=["Interface Web Acceuil"])
def read_root(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("Interface_Web.html", {"request": request})
# Route pour afficher la page méteo

@app.get("/meteo", response_class=HTMLResponse, tags=["Interface Web Météo"])
def get_meteo_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("meteo.html", {"request": request})
# Route pour la page logement
@app.get("/logements", response_class=HTMLResponse, tags=["Interface Web Logements"])
def get_logements_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("logement.html", {"request": request})
# Route pour la page pieces
@app.get("/pieces", response_class=HTMLResponse, tags=["Interface Web Pièces"])
def get_pieces_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("pieces.html", {"request": request})
#Route pour la page mesures
@app.get("/mesures", response_class=HTMLResponse, tags=["Interface Web Mesures"])
def get_mesures_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("mesures.html", {"request": request})

# Route pour la piece spécifique pour un logement 
@app.get("/pieces/{logement_id}", status_code=status.HTTP_200_OK, tags=["Pièces"])
def get_pieces_by_logement(logement_id: int, session: Session = Depends(get_session)):
    pieces = session.exec(select(Piece).where(Piece.logement_id == logement_id)).all()
    if not pieces:
        raise HTTPException(status_code=404, detail="Aucune pièce trouvée pour ce logement")
    return {"pieces": pieces}
# route vers la page capteur
@app.get("/capteurs", response_class=HTMLResponse, tags=["Interface Web Capteurs"])
def get_capteurs_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("capteurs.html", {"request": request})
#route vers la page actions
@app.get("/actions-web", response_class=HTMLResponse, tags=["Interface Web Actions"])
def get_actions_page(request: Request):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("actions.html", {"request": request})

# route vers la page factures 
@app.get("/facture", response_class=HTMLResponse, tags=["Interface Web Factures"])
def get_factures_page(request: Request, logement_id: int):
    templates = Jinja2Templates(directory="C:/Users/oumer/Desktop/IOT/LOGEMENTECO-RESPONSABLE/code/templates")
    return templates.TemplateResponse("facture.html", {"request": request, "logement_id": logement_id})


# capteur pour chaque pieces 
@app.get("/capteur-actionneur-pieces", status_code=status.HTTP_200_OK, tags=["Capteur Actionneur-pieces"])
def read_capteurs_by_piece(piece_id: int, session: Session = Depends(get_session)):
    """
    Retourne les capteurs actionneurs spécifiques à une pièce donnée.
    """
    capteurs = session.exec(select(capteur_actionneur).where(capteur_actionneur.piece_id == piece_id)).all()
    if not capteurs:
        raise HTTPException(status_code=404, detail=f"Aucun capteur trouvé pour la pièce ID {piece_id}")
    return {"capteurs": capteurs}
# route vers mesure de chaque capteur
@app.get("/mesure-capteur/{capteur_id}", status_code=status.HTTP_200_OK, tags=["Mesures"])
def read_mesures(capteur_id: int, session: Session = Depends(get_session)):
    mesures = session.exec(
        select(Mesure).where(Mesure.capteur_actionneur_id == capteur_id)
    ).all()
    if not mesures:
        raise HTTPException(status_code=404, detail="Aucune mesure trouvée pour ce capteur.")
    return {"mesures": mesures}
# route action-capteur
@app.get("/actions-capteur/{capteur_id}", status_code=status.HTTP_200_OK, tags=["Actions"])
def read_actions(capteur_id: int, session: Session = Depends(get_session)):
    actions = session.exec(
        select(Action).where(Action.capteur_id == capteur_id)
    ).all()
    if not actions:
        raise HTTPException(status_code=404, detail="Aucune action trouvée pour ce capteur.")
    return {"actions": actions}
#facture (logement)
@app.get("/factures-logement", response_model=List[Facture], tags=["Factures"])
def get_factures(logement_id: int, session: Session = Depends(get_session)):
    """
    Récupère les factures d'un logement spécifique.
    """
    factures = session.exec(select(Facture).where(Facture.logement_id == logement_id)).all()
    if not factures:
        raise HTTPException(status_code=404, detail="Aucune facture trouvée pour ce logement.")
    return factures


# Routes pour Logement
@app.post("/logement", status_code=status.HTTP_201_CREATED, tags=["Logement"])
def create_logement(logement: Logement, session: Session = Depends(get_session)):
    logement.date_insertion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.add(logement)

    session.commit()
    session.refresh(logement)
    return {"message": "Logement ajouté", "logement": logement}

@app.get("/logement", status_code=status.HTTP_200_OK, tags=["logement"])
def read_LOGEMENT(session: Session = Depends(get_session)):
    LogementS = session.exec(select(Logement)).all()
    return {"logement": LogementS}

# Routes pour Piece
@app.post("/piece", status_code=status.HTTP_201_CREATED, tags=["Pièces"])
def create_piece(piece: Piece, session: Session = Depends(get_session)):
    logement = session.get(Logement, piece.logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    session.add(piece)
    session.commit()
    session.refresh(piece)
    return {"message": "Pièce ajoutée", "piece": piece}

@app.get("/piece", status_code=status.HTTP_200_OK, tags=["Pièces"])
def read_pieces(session: Session = Depends(get_session)):
    pieces = session.exec(select(Piece)).all()
    return {"pieces": pieces}

# Routes pour TypeCapteurActionneur
@app.post("/type-capteur-actionneur", status_code=status.HTTP_201_CREATED, tags=["Types de Capteurs"])
def create_type_capteur(type_capteur: type_capteur_actionneur, session: Session = Depends(get_session)):
    session.add(type_capteur)
    session.commit()
    session.refresh(type_capteur)
    return {"message": "Type ajouté", "type_capteur": type_capteur}

@app.get("/type-capteur-actionneur", status_code=status.HTTP_200_OK, tags=["Types de Capteurs"])
def read_type_capteurs(session: Session = Depends(get_session)):
    types = session.exec(select(type_capteur_actionneur)).all()
    return {"type_capteurs": types}

# Routes pour CapteurActionneur
@app.post("/capteur-actionneur", status_code=status.HTTP_201_CREATED ,  tags=["Capteur Actionneur"])
def create_capteur(capteur: capteur_actionneur, session: Session = Depends(get_session)):
    piece = session.get(Piece, capteur.piece_id)
    type_capteur = session.get(type_capteur_actionneur, capteur.type_id)
    if not piece or not type_capteur:
        raise HTTPException(status_code=404, detail="Pièce ou type capteur non trouvé")
    capteur.date_insertion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.add(capteur)
    session.commit()
    session.refresh(capteur)
    return {"message": "Capteur ajouté", "capteur": capteur}

@app.get("/capteur-actionneur", status_code=status.HTTP_200_OK , tags=["Capteur Actionneur"])
def read_capteurs(session: Session = Depends(get_session)):
    capteurs = session.exec(select(capteur_actionneur)).all()
    return {"capteurs": capteurs}
# Routes pour Mesure
@app.post("/mesure", status_code=status.HTTP_201_CREATED, tags=["Mesures"])
def create_mesure(mesure: Mesure, session: Session = Depends(get_session)):
    capteur = session.get(capteur_actionneur, mesure.capteur_actionneur_id)
    if not capteur:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")

    mesure.date_insertion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.add(mesure)
    session.commit()
    session.refresh(mesure)

    # Vérifier les conditions et créer des actions automatiques
    type_capteur = session.get(type_capteur_actionneur, capteur.type_id)
    if type_capteur.nom == "température":
        external_temp = get_external_temperature()
        action_type = "Allumer LED" if mesure.valeur < external_temp else "Éteindre LED"
        session.add(Action(capteur_id=capteur.id, type_action=action_type, date_insertion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        session.commit()

    return {"message": "Mesure ajoutée avec actions automatiques", "mesure": mesure}

@app.get("/mesure", status_code=status.HTTP_200_OK, tags=["Mesures"])
def read_mesures(session: Session = Depends(get_session)):
    mesures = session.exec(select(Mesure)).all()
    return {"mesures": mesures}

# Routes pour Factures
@app.post("/factures", status_code=status.HTTP_201_CREATED, tags=["Factures"])
def create_facture(facture: Facture, session: Session = Depends(get_session)):
    session.add(facture)
    session.commit()
    session.refresh(facture)
    return {"message": "Facture ajoutée avec succès", "facture": facture}

@app.get("/factures", status_code=status.HTTP_200_OK, tags=["Factures"])
def read_factures(session: Session = Depends(get_session)):
    factures = session.exec(select(Facture)).all()
    return {"factures": factures}
# Routes pour les actions
@app.get("/actions", status_code=status.HTTP_200_OK, tags=["Actions"])
def read_actions(session: Session = Depends(get_session)):
    actions = session.exec(select(Action)).all()
    return {"actions": actions}

# Lancer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
