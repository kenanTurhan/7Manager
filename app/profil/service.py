from fastapi import APIRouter, HTTPException, Depends
from app.dependance import utilisateur_courant
from app.core.database import supabase



def information(claims):
    data = supabase.table("utilisateur").select("*").eq("id", claims["sub"]).execute()
    if not data.data:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return data.data[0]

def modifierUtilisateur(claims, nom, prenom, date_naissance, taille_cm, poid_kg, poste):
    response = (
    supabase.table("utilisateur")
    .update({"nom": nom, "prenom": prenom, "date_naissance": date_naissance, "taille_cm": taille_cm, "poid_kg": poid_kg, "poste_prefere":poste})
    .eq("id", claims["sub"])
    .execute()
    )
    
    return response

