from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
from fastapi import HTTPException
from postgrest.exceptions import APIError


def creerEquipe(claims, nom, description, couleur1, couleur2, urlImage, codePostal):
    id = claims.get("sub")
    user = supabase.table("utilisateur").select("*").eq("id", id).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="Cette action nessecite une connexion")
    else:
        response = (
            supabase.table("club")
            .insert({"nom": nom, "description": description, "couleur1":couleur1, "couleur2":couleur2, "urlImage": urlImage, "codePostal":codePostal})
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

