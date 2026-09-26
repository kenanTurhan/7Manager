from pydantic import BaseModel

class creerEquipe(BaseModel):
    nom: str
    description: str
    couleur1: str
    couleur2: str
    urlImage: str
    codePostal: str
    division: str

