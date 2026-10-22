from fastapi import APIRouter, HTTPException, Depends
from app.match import services as service
import app.match.models as modeles
from app.dependance import utilisateur_courant
from app.core.database import supabase, get_supabase


router = APIRouter(prefix= "/match", tags=["match"])

@router.post("/creerMatch")
def creerMatch(match: modeles.preMatch, claim=Depends(utilisateur_courant)):
    return service.creerMatch(match.recevant, match.visiteur, match.date, match.heure, match.division, match.stade, claim)

@router.get("/match")
def matchDuJours():
    return service.matchDuJour()

@router.get("/matchParJour")
def matchParJours(date: str):
    return service.matchParJour(date)

@router.patch("/match")
def modifierMatch(idMatch:str, match: modeles.preMatch, claim=Depends(utilisateur_courant)):
    return service.modifierMatch(idMatch, match.recevant, match.visiteur, match.date, match.heure, match.division, match.stade, claim)

@router.patch("/faitDeJeu")
def faitDeJeu(matchId: str, faitDeJeu :  modeles.faitDeJeu, claim = Depends(utilisateur_courant)):
    return service.faitDeJeu(matchId, faitDeJeu.autheurEquipe, faitDeJeu.buteurJoueur, faitDeJeu.passeurJoueur, faitDeJeu.minute, claim)