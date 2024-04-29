from typing import Union
from firebase_admin import auth

# Drf Easily Saas
from drf_easily_saas.schemas.claims import ClaimsPayment


def add_custom_claims(uid: str, claims: dict) -> Union[auth.UserRecord, None]:
    """
    Add custom claims to a Firebase user.
    """
    # Validate claims
    claims_validation = ClaimsPayment(**claims)
    if not claims_validation:
        return None
    # Add custom claims
    auth.set_custom_user_claims(uid, claims_validation.dict())
    # Check if claims are added
    if auth.get_user(uid).custom_claims == claims:
        # Ici on force la mise à jour du token pour que les nouvelles informations soient prises en compte
        # Ce qui à pour effet deconnecter le user de toutes ses sessions sur tous les devices
        # Il devra se reconnecter pour obtenir un nouveau token
        # Cela assure que les nouvelles informations sont prises en compte rapidement
        auth.revoke_refresh_tokens(uid)
        return auth.get_user(uid)
    return None