from fastapi import APIRouter, HTTPException
from app.postes import service
import app.postes.models as modeles
router = APIRouter(prefix= "/postes", tags=["postes"])

@router.get("/hello")
def helloWord():
    return "helloWord"

@router.post("/ajouter_poste")
def ajouter_poste(poste:modeles.ajouterPoste):
    try:
        resultat = service.func_ajouter_poste(poste.poste)
        return {"message": f"poste {poste.poste} ajouter"}
    except HTTPException:
        raise

@router.delete("/retirer_poste")
def retirer_poste(poste:modeles.retirerPoste):
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
def actualiser_poste(data:modeles.modifierPoste):
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

