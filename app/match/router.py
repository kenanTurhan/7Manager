from fastapi import APIRouter, HTTPException, Depends
from app.match import services as service
import app.match.models as modeles
from app.dependance import utilisateur_courant
from app.core.database import supabase, get_supabase


router = APIRouter(prefix= "/match", tags=["match"])

@router.post("/creerMatch")
def creerMatch(match: modeles.preMatch, claim=Depends(utilisateur_courant)):
    return service.creerMatch(match.recevant, match.visiteur, match.date, match.heure, match.division, match.stade, claim)

@router.get("/matchDuJour")
def matchDuJours(date: str):
    return service.matchDuJour(date)