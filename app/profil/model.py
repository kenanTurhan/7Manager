from pydantic import BaseModel

class modifierNom(BaseModel):
    nom: str
    prenom: str
    date_naissance: str
    taille_cm: int
    poid_kg: int
    poste_prefere: str

