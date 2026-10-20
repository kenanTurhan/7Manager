from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
from fastapi import HTTPException
from postgrest.exceptions import APIError
import secrets


def creerMatch(recevant, visiteur, date, heure, division, stade, claim):
    #recuperer userId
    userId = claim["sub"]
    #vérifier role admin appli
    admin = supabase.table("utilisateur").select("admin").eq("id", userId).eq("admin", True).execute()
    if not admin.data:
        raise HTTPException(status_code=403, detail="Vous devez être administrateur de l'application pour créer un match")
    supabase.table("match").insert({"club_recevant": recevant, "club_visiteur":visiteur, "date_match": date.isoformat(), "heure_match":heure.isoformat(), "match_division":division, "stade":stade, "fini":False}).execute()

    return(f"le match opposant {recevant} à {visiteur} a bien été enregistrer")

def matchDuJour(date):
    match = supabase.table("match").select("club_recevant", "club_visiteur", "date_match", "heure_match", "stade", "match_division").eq("date_match", date).execute()
    return match.data


