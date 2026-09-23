from fastapi import APIRouter, HTTPException, Depends
from app.postes import service
import app.postes.models as modeles
from app.dependance import utilisateur_courant
from app.core.database import supabase, get_supabase
 

router = APIRouter(prefix= "/postes", tags=["postes"])

@router.get("/hello")
def helloWord():
    return "helloWord"

@router.post("/ajouter_poste")
def ajouter_poste(poste: modeles.ajouterPoste, claims=Depends(utilisateur_courant)):
    id = claims.get("sub")
    response = (
        supabase.table("utilisateur")
        .select("admin")
        .eq("id", id)
        .execute()
    )

    if not response.data or not response.data[0]["admin"]:
        raise HTTPException(status_code=403, detail="Cette action est réservée aux administrateurs")
    else:
        try:
            resultat = service.func_ajouter_poste(poste.poste)
            return {"message": f"poste {poste.poste} ajouter"}
        except HTTPException:
            raise

    return response.data[0]["admin"]    

@router.delete("/retirer_poste")
def retirer_poste(poste:modeles.retirerPoste, claims=Depends(utilisateur_courant)):
    id = claims.get("sub")
    response = (
        supabase.table("utilisateur")
        .select("admin")
        .eq("id", id)
        .execute()
    )

    if not response.data or not response.data[0]["admin"]:
        raise HTTPException(status_code=403, detail="Cette action est réservée aux administrateurs")
    else:

        try:
            resultat = service.func_retirer_poste(poste.poste)
            if isinstance(resultat, dict) and "error" in resultat:
                raise HTTPException(status_code=500, detail=resultat["error"])
            if not resultat:
                raise HTTPException(status_code=404, detail=f"poste {poste.poste} non trouvé")
            return {"message": f"poste {poste.poste} retirer"}
            
        except HTTPException:
            raise
        except Exception as e:  
            raise HTTPException(status_code=500, detail=str(e))


@router.patch("/actualiser_poste")
def actualiser_poste(data:modeles.modifierPoste, claims = Depends(utilisateur_courant)):
    id = claims.get("sub")
    response = (
        supabase.table("utilisateur")
        .select("admin")
        .eq("id", id)
        .execute()
    )
    if not response.data or not response.data[0]["admin"]:
        raise HTTPException(status_code=403, detail="Cette action est réservée aux administrateurs")
    else:
        try:
            resultat = service.func_actualiser_poste(data.poste, data.nouveauPoste)
            if isinstance(resultat, dict) and "error" in resultat:
                raise HTTPException(status_code=500, detail=resultat["error"])
            if not resultat:
                raise HTTPException(status_code=404, detail=f"poste {data.poste} non trouvé")
            return {"message": f"poste {data.poste} actualisé"}      
        except HTTPException:
            raise
        except Exception as e:  
            raise HTTPException(status_code=500, detail=str(e))

