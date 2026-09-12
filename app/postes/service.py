from app.core.database import supabase

def func_ajouter_poste(poste:str):
    try:
        reponse = supabase.table("poste").insert({"poste":poste}).execute()
        return reponse.data
    except Exception as e:
        return {"error": str(e)}

def func_retirer_poste(poste:str):
    try:
        reponse = supabase.table("poste").delete().eq("poste",poste).execute()
        return reponse.data
    except Exception as e:
        return {"error": str(e)}

def func_actualiser_poste(poste:str, nouveauPoste:str):
    try:
        reponse = supabase.table("poste").update({"poste":nouveauPoste}).eq("poste",poste).execute()
        return list(reponse.data)
    except Exception as e:
        return {"error": str(e)}
        