from fastapi import APIRouter
router = APIRouter(prefix= "/auth", tags=["Auth"])
import app.auth.models as model
import app.auth.service as service


@router.post("/inscription",    response_model=model.InscriptionOut,
 responses={400: {"description": "Inscription impossible"}},
)
def inscritpion(reponse:model.inscription):
    response = service.inscription(
        mail=reponse.mail,
        motPasse=reponse.motPasse,
        nom=reponse.nom,
        prenom=reponse.prenom,
        date_naissance=reponse.date_naissance,
        poste_prefere=reponse.poste_prefere,
        taille_cm=reponse.taille_cm,
        poids_kg=reponse.poids_kg
    )
    return response

@router.post("/connexion", response_model=model.ConnexionOut,
 responses={400: {"description": "Connexion impossible"}},
)
def connexion(reponse:model.connexion):
    response = service.connexion(
        email=reponse.email,
        motPasse=reponse.motPasse,
    )
    return response
