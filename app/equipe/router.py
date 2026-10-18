from fastapi import APIRouter, HTTPException, Depends
from app.equipe import service as service
import app.equipe.models as modeles
from app.dependance import utilisateur_courant
from app.core.database import supabase, get_supabase


router = APIRouter(prefix= "/equipe", tags=["equipe"])

@router.post("/creer_equipe")
def creer_equipe(equipe: modeles.creerEquipe, claims=Depends(utilisateur_courant)):
    # Crée l'équipe
    idClub = service.creerEquipe(claims, equipe.nom, equipe.description, equipe.couleur1, equipe.couleur2, equipe.urlImage, equipe.codePostal, equipe.division)
    # Ajoute le créateur dans le club via la table appartenirClub, en temps qu'admin et capitaine
    return service.ajouterJoueurClubCreation(claims, idClub)

@router.get("/membre")
def getMembre(idEquipe: int, claims=Depends(utilisateur_courant)):
    return service.listeJoueurEquipe(idEquipe)

@router.post("/creerCodeInvitation")
def creerCodeInvitation(equipe: modeles.inviterEquipe, claims=Depends(utilisateur_courant)):
    return service.inviterEquipe(claims, equipe.idEquipe)

@router.post("/rejoindreEquipe")
def rejoindreEquipe(code:modeles.rejoindre, claims=Depends(utilisateur_courant)):
    return service.rejoindreClub(claims, code.codeInvitation)

@router.get("/infoEquipe")
def getEquipe(idEquipe: str, claims=Depends(utilisateur_courant)):
    return service.infoEquipe(idEquipe)


# Liste de mes équipes

@router.get("/mesEquipes")
def mesEquipes(claims=Depends(utilisateur_courant)):
    return service.mesEquipes(claims)

# Modifier une équipe (admin)
@router.patch("modifierEquipe")
def modifierEquipe(idEquipe:str, modif: modeles.modifierEquipe, claims=Depends(utilisateur_courant)):
    return service.modifierEquipe(claims, modif.nom, modif.description, modif.couleur1, modif.couleur2, modif.urlImage, modif.codePostal, modif.division, idEquipe)
# Supprimer une équipe (admin)

@router.delete("/supprimerEquipe")
def supprimerEquipe(idEquipe, claim = Depends(utilisateur_courant)):
    return service.supprimerEquipe(idEquipe, claim)


# promouvoir admin
@router.patch("/promouvoirAdmin")
def promouvoirAdmin(idEquipe, idJoueur, claims=Depends(utilisateur_courant)):
    return service.promouvoirAdmin(idEquipe, idJoueur, claims)


# Retirer un membre (admin)
@router.delete("/supprimerMembre")
def supprimerMembre(idEquipe, idJoueur, claims=Depends(utilisateur_courant)):
    return service.supprimerMembre(idEquipe, idJoueur, claims) 

