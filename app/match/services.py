from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
from fastapi import HTTPException
from postgrest.exceptions import APIError
import secrets
from datetime import datetime


def creerMatch(recevant, visiteur, date, heure, division, stade, claim):
    #recuperer userId
    userId = claim["sub"]
    #vérifier role admin appli
    admin = supabase.table("utilisateur").select("admin").eq("id", userId).eq("admin", True).execute()
    if not admin.data:
        raise HTTPException(status_code=403, detail="Vous devez être administrateur de l'application pour créer un match")

    #modifier le match
    supabase.table("match").insert({"club_recevant": recevant, "club_visiteur":visiteur, "date_match": date.isoformat(), "heure_match":heure.isoformat(), "match_division":division, "stade":stade, "fini":False}).execute()

    return(f"le match opposant {recevant} à {visiteur} a bien été enregistrer")

def matchDuJour():
    date = datetime.today().strftime('%Y-%m-%d')

    match = supabase.table("match").select("id", "club_recevant", "club_visiteur", "date_match", "heure_match", "stade", "match_division").eq("date_match", date).execute()
    return match.data


def matchParJour(date):
    match = supabase.table("match").select("id", "club_recevant", "club_visiteur", "date_match", "heure_match", "stade", "match_division").eq("date_match", date).execute()
    return match.data

def modifierMatch(idMatch, recevant, visiteur, date, heure, division, stade, claim):
    #recuperer userId
    userId = claim["sub"]
    #vérifier role admin appli
    admin = supabase.table("utilisateur").select("admin").eq("id", userId).eq("admin", True).execute()
    if not admin.data:
        raise HTTPException(status_code=403, detail="Vous devez être administrateur de l'application pour modifier un match")

    #vérifie l'existance du match
    match = supabase.table("match").select(id).eq("id", id).execute()
    if not match.data:
        raise HTTPException(status_code=404, detail="Le match à modifier n'éxiste pas")

    #modifier le match
    supabase.table("match").update({"club_recevant": recevant, "club_visiteur":visiteur, "date_match": date.isoformat(), "heure_match":heure.isoformat(), "match_division":division, "stade":stade}).eq("id", idMatch).execute()
    return(f"le match opposant {recevant} à {visiteur} a bien été modifié")



