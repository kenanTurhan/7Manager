from pydantic import BaseModel

class creerEquipe(BaseModel):
    nom: str
    description: str
    couleur1: str
    couleur2: str
    urlImage: str
    codePostal: int
    division: str

class inviterEquipe(BaseModel):
    idEquipe: str

class rejoindre(BaseModel):
    codeInvitation: int

class modifierEquipe(BaseModel):
    nom: str
    description: str
    couleur1: str
    couleur2: str
    urlImage: str
    codePostal: int
    division: str
