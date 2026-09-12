from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class inscription(BaseModel):
    mail:str
    motPasse: str
    nom:str
    prenom:str
    date_naissance:str
    poste_prefere:str
    taille_cm:int
    poids_kg:int

class InscriptionOut(BaseModel):
    id: str
    email: str

class connexion(BaseModel):
    email: str
    motPasse: str

class UtilisateurOut(BaseModel):
    id: str
    email: str
    nom: str
    prenom: str
    date_naissance: str
    poste_prefere: str
    taille_cm: int
    poid_kg: Optional[int] = None
    role: str
    profil_complet: bool
    admin: bool
    cree_le: datetime
    maj_le: datetime

class ConnexionOut(BaseModel):
    id: str
    email: str
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    utilisateur: UtilisateurOut


    
    