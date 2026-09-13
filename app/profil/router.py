from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
import app.profil.service  as serviceInformation
import app.profil.model as model

router = APIRouter(prefix= "/profil", tags=["profile"])


@router.get("/information")
def information(claims = Depends(utilisateur_courant)):
    try:
        response = serviceInformation.information(claims)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/modifierUtilisateur")
def modifierInformation(user:model.modifierNom,claims = Depends(utilisateur_courant)):
    try:
        response = serviceInformation.modifierUtilisateur(claims, user.nom, user.prenom, user.date_naissance, user.taille_cm, user.poid_kg, user.poste_prefere)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
