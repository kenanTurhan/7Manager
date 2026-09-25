from fastapi import APIRouter, HTTPException, Depends
from app.equipe import service as service
import app.equipe.models as modeles
from app.dependance import utilisateur_courant
from app.core.database import supabase, get_supabase


router = APIRouter(prefix= "/equipe", tags=["equipe"])

@router.post("/creer_equipe")
def creer_equipe(equipe: modeles.creerEquipe, claims=Depends(utilisateur_courant)):
    # Crée l'équipe
    idClub = service.creerEquipe(claims, equipe.nom, equipe.description, equipe.couleur1, equipe.couleur2, equipe.urlImage, equipe.codePostal)
    # Ajoute le créateur dans le club via la table appartenirClub, en temps qu'admin et capitaine
    return service.ajouterJoueurClubCreation(claims, idClub)
