from app.core.database import supabase, get_supabase
from fastapi import HTTPException
from supabase_auth.errors import AuthError


def inscription(mail:str, motPasse:str, nom:str, prenom:str, date_naissance:str, poste_prefere:str, taille_cm:int, poids_kg:int):
    try:
        response = get_supabase().auth.sign_up(
                {
                    "email": mail,
                    "password": motPasse,   
                    "options":{
                        "data":{
                            "nom": nom,
                            "prenom": prenom,
                            "date_naissance": date_naissance,
                            "poste_prefere": poste_prefere,
                            "taille_cm": taille_cm,
                            "poids_kg": poids_kg
                        }
                    }
                }        )
    except AuthError as e:
        raise HTTPException(status_code=getattr(e, "status", None) or 400, detail=e.message)

    if not response.user:
        raise HTTPException(status_code=400, detail="Inscription impossible")

    return {"id": response.user.id, "email": response.user.email}


def connexion(email:str, motPasse:str):
    try:
        response = get_supabase().auth.sign_in_with_password(
            {
                "email": email,
                "password": motPasse,
            }
        )
    except AuthError as e:
        raise HTTPException(status_code=getattr(e, "status", None) or 400, detail=e.message)

    if not response.user or not response.session:
        raise HTTPException(status_code=400, detail="Connexion impossible")

    utilisateur = (
        supabase.table("utilisateur")
        .select("*")
        .eq("id", response.user.id)
        .execute()
    )

    if not utilisateur.data:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    utilisateur_data = utilisateur.data[0]

    return {
        "id": response.user.id,
        "email": response.user.email,
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "token_type": response.session.token_type,
        "expires_in": response.session.expires_in,
        "utilisateur": utilisateur_data,
    }


