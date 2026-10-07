from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
from fastapi import HTTPException
from postgrest.exceptions import APIError
import random

random.seed(1)

def creerEquipe(claims, nom, description, couleur1, couleur2, urlImage, codePostal, division):
    id = claims.get("sub")
    user = supabase.table("utilisateur").select("*").eq("id", id).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="Cette action nessecite une connexion")
    else:
        response = (
            supabase.table("club")
            .insert({"nom": nom, "description": description, "couleur1":couleur1, "couleur2":couleur2, "urlImage": urlImage, "codePostal":codePostal, "division": division})
            .execute()
            )
        return response.data[0]["id"]   

def ajouterJoueurClubCreation(claims, idClub):
    print(idClub)
    id = claims.get("sub")
    user = supabase.table("utilisateur").select("*").eq("id", id).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="Cette action nessecite une connexion")
    else:
        try:

            reponse = supabase.table("appartenirEquipe").insert({"idJoueur": id, "idClub": idClub, "estCapitaine": True, "estAdmin": True}).execute()
            return reponse

        except APIError as e:
            raise HTTPException(status_code=400, detail=e.message)

def listeJoueurEquipe(idEquipe):
    try:
        reponse = (supabase.table("appartenirEquipe").select("idJoueur").eq("idClub", idEquipe).execute())
        return reponse
    except APIError as e:
        raise HTTPException(status_code=400, detail=e.message)

def inviterEquipe(claims, idEquipe):
    idJoueur = claims.get("sub")

    admin = (
        supabase.table("appartenirEquipe")
        .select("estAdmin")
        .eq("idJoueur", idJoueur)
        .eq("idClub", idEquipe)
        .eq("estAdmin", True)
        .execute()
    )
    if not admin.data:
        raise HTTPException(status_code=403, detail="Cette action nécessite d'être administrateur du club")
    try:
        codeInvitation = random.randint(0, 9999)
        response = supabase.table("club").update({"codeInvitationTemporaire": codeInvitation}).eq("id", idEquipe).execute()
    except APIError as e:
        # Erreur côté base : colonne inexistante, type invalide, droits RLS...
        raise HTTPException(status_code=400, detail=e.message)
    except Exception:
        # Erreur imprévue : réseau, Supabase injoignable...
        raise HTTPException(status_code=500, detail="Erreur serveur")

    # Aucune ligne modifiée, donc le club n'existe pas
    if not response.data:
        raise HTTPException(status_code=404, detail="Club introuvable")

    return {"code": codeInvitation}     

def rejoindreClub(claims, codeInvitation):
    id = claims.get("sub")
    clubId = supabase.table("club").select("id").eq("codeInvitationTemporaire", codeInvitation).execute()
    if not clubId.data:
        raise HTTPException(status_code=404, detail="Invitation expirer ou innexistante")
    query = supabase.table("appartenirEquipe").select("*").eq("idJoueur", id).eq("idClub", clubId.data[0]["id"]).execute()
    if query.data:
        raise HTTPException(status_code=400, detail="Vous êtes déjà membre de ce club")
    try:
        response = (
            supabase.table("appartenirEquipe")
            .insert({"idJoueur":id, "idClub": clubId.data[0]["id"],"estCapitaine": False, "estAdmin": False})
            .execute()
        )
    except APIError as e:
        raise HTTPException(status_code=400, detail=e.message)

def infoEquipe(idEquipe):
    try:
        query = supabase.table("club").select("nom", "description", "couleur1", "couleur2", "urlImage", "codePostal", "division").eq("id", idEquipe).execute()
    except:
        raise HTTPException(status_code=404, detail="Equipe introuvable")

    return query