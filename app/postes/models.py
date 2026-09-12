from pydantic import BaseModel

class ajouterPoste(BaseModel):
    poste: str

class retirerPoste(BaseModel):
    poste: str

class modifierPoste(BaseModel):
    poste: str
    nouveauPoste:str