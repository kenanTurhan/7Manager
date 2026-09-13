# app/dependances.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_supabase  

securite = HTTPBearer()

def utilisateur_courant(cred: HTTPAuthorizationCredentials = Depends(securite)):
    try:
        res = get_supabase().auth.get_claims(cred.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")

    if not res:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    claims = res["claims"] if isinstance(res, dict) and "claims" in res else res
    return claims