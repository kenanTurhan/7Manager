from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase
from fastapi import HTTPException
from postgrest.exceptions import APIError
import secrets


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
        codeInvitation = secrets.randbelow(10000)
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
    return("Vous avez bien rejoint l'équipe")

def infoEquipe(idEquipe):
    try:
        query = supabase.table("club").select("nom", "description", "couleur1", "couleur2", "urlImage", "codePostal", "division").eq("id", idEquipe).execute()
    except:
        raise HTTPException(status_code=404, detail="Equipe introuvable")
 
    return query

def mesEquipes(claims):
    userId = claims["sub"]
    try:
        query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).execute()
        return query
    except:
        raise HTTPException(status_code=404, detail="Vous devez vous connecter")

def modifierEquipe(claims, nom, description, couleur1, couleur2, urlImage, codePostal, division, idEquipe):
    #verifier qu'on est admin
    userId = claims["sub"]
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).eq("idClub", idEquipe).eq("estAdmin", True).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Cette action necessite des droit administrateurs")
    
    update = supabase.table("club").update({"nom": nom, "description":description, "couleur1": couleur1, "couleur2": couleur2, "urlImage":urlImage, "codePostal":codePostal, "division":division} ).eq("id", idEquipe).execute()

    
    return(query)


def supprimerEquipe(idEquipe, claims):
    #verifier qu'on est admin
    userId = claims["sub"]
    #le club existe il
    query = supabase.table("club").select("nom").eq("id", idEquipe).execute()
    if not query.data:
        raise HTTPException(status_code=404, detail="Le club existe pas")
    #check role admin
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).eq("idClub", idEquipe).eq("estAdmin", True).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Cette action necessite des droit administrateurs")
    #supprimer la liste des membres:
    delete = supabase.table("appartenirEquipe").delete().eq("idClub", idEquipe).execute()
    #supprimer l'équipe
    delete = supabase.table("club").delete().eq("id", idEquipe).execute()

    return("le club à bien été supprimé")


def promouvoirAdmin(idEquipe, idJoueur, claims):
    userId = claims["sub"]
    #check role admin
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).eq("idClub", idEquipe).eq("estAdmin", True).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Cette action necessite des droit administrateurs")
    #verifier qu'on promote supprime pas
    if userId == idJoueur:
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas vous auto promouvoir.")

    #verifie que e joueur à promouvoir existe
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", idJoueur).eq("idClub", idEquipe).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Le joueur n'existe pas")
    #verifie que le joueur à promouvoir ne soit pas déjà admin
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", idJoueur).eq("idClub", idEquipe).eq("estAdmin", False).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Le joueur est déjà admin")

    supabase.table("appartenirEquipe").update({"estAdmin": True}).eq("idJoueur", idJoueur).eq("idClub", idEquipe).execute()

    return("Le joueur à bien été promus")


def supprimerMembre(idEquipe, idJoueur, claims):
    userId = claims["sub"]
   
    #check role admin
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).eq("idClub", idEquipe).eq("estAdmin", True).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Cette action necessite des droit administrateurs")
    
    #verifier qu'on s'auto supprime pas
    if userId == idJoueur:
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas vous auto supprimer. Passez par l'option 'quitter le club' ")
    
    #verifie que e joueur à supprimer existe
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", idJoueur).eq("idClub", idEquipe).execute()
    if not query.data:
        raise HTTPException(status_code=403, detail="Le joueur n'existe pas")
    
    #verifie que le joueur supprimer ne soit pas admin 
    query = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", idJoueur).eq("idClub", idEquipe).eq("estAdmin", False).execute()
    if not query.data:
        capitaine = supabase.table("appartenirEquipe").select("idClub").eq("idJoueur", userId).eq("idClub", idEquipe).eq("estCapitaine", True).execute()
        if not capitaine.data:
            raise HTTPException(status_code=403, detail="Le joueur est admin, seul le capitaine peut le supprimer")

    supabase.table("appartenirEquipe").delete().eq("idJoueur", idJoueur).eq("idClub", idEquipe).execute()

    return("Le joueur à bien été supprimé de l'équipe")

def capitana(idEquipe, idJoueur, claims):
    userId = claims["sub"]
    #vérifier que le joueur est bien l'actuel capitaine
    capitaineActuel = supabase.table("appartenirEquipe").select("id").eq("idClub", idEquipe).eq("idJoueur", userId).eq("estCapitaine", True).execute()
    if not capitaineActuel.data:
        raise HTTPException(status_code=403, detail="Seul le capitaine peut transferer le role de capitaine")
    #vérifie que le joueur à capitainer est membre du club
    joueur = supabase.table("appartenirEquipe").select("id").eq("idClub", idEquipe).eq("idJoueur", idJoueur).execute()
    if not joueur.data:
        raise HTTPException(status_code=404, detail="Le joueurs à promouvoir n'existe pas")

    #passer l'encien capitaine en joueur
    supabase.table("appartenirEquipe").update({"estCapitaine": False}).eq("idClub", idEquipe).eq("idJoueur", userId).execute()

    #passer le nouveau capitaine en capitaine
    supabase.table("appartenirEquipe").update({"estCapitaine": True}).eq("idClub", idEquipe).eq("idJoueur", idJoueur).execute()
    nom = supabase.table("utilisateur").select("nom").eq("id", idJoueur).execute()

    return f"Le brassard a été transféré à {nom.data[0]['nom']}"    


def quitterEquipe(idEquipe, claims):
    #get id joueur
    idJoueur = claims["sub"]

    #vérifier que le joueur fait bien partie de l'équipe
    verifEquipe = supabase.table("appartenirEquipe").select("id").eq("idClub",idEquipe).eq("idJoueur", idJoueur).execute()
    if not verifEquipe.data:
        raise HTTPException(status_code=403, detail="Vous ne faites pas partie de l'équipe que vous voulez quitter.")

    #vérifie que l'on soit pas capitaine
    verifCapitaine = supabase.table("appartenirEquipe").select("id").eq("idClub",idEquipe).eq("idJoueur", idJoueur).eq("estCapitaine", True).execute()
    if verifCapitaine.data:
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas quitter l'équipe en étant capitaine, veuillez d'abord nommer un nouveau capitaine.")

    #quitter
    delete = supabase.table("appartenirEquipe").delete().eq("idClub", idEquipe).eq("idJoueur", idJoueur).execute()

    return("Vous avez bien quitté l'équipe.")