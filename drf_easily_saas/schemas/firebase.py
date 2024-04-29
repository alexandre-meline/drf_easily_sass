import os
import json
import firebase_admin
from firebase_admin import credentials
from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

# Drf Easily Saas
from drf_easily_saas.exceptions.firebase import InvalidFirebaseConfigurationError
from drf_easily_saas.utils.db import (
    check_table_exists, 
    check_table_empty
    )
from drf_easily_saas.auth.firebase.protect import import_users


# -------------------------------------------- #
# Firebase settings schema validation
# -------------------------------------------- #
class FirebaseConfig(BaseModel):
    """
    This class is used to validate the Firebase configuration.

    On this class, we validate the Firebase configuration and import users from Firebase if import_users is True.

    Args:
    - config (Union[str, Dict[str, Any]]): Firebase configuration
    - import_users (bool): Import users from Firebase

    Returns:
    - config (Union[str, Dict[str, Any]]): Firebase configuration
    - import_users (bool): Import users from Firebase
    """
    config: Union[str, Dict[str, Any]]
    import_users: bool
    hot_reload_import: bool = False
    
    @field_validator('config')
    def validate_config(cls, v):
        config = None
        # This is a file path
        if isinstance(v, str):
            if os.path.exists(v):
                with open(v, 'r') as f:
                    config_file =  f.read()
                    try:
                        config = json.loads(config_file)
                    except json.JSONDecodeError:
                        raise InvalidFirebaseConfigurationError("Firebase config is not a valid JSON")
            else:
                raise InvalidFirebaseConfigurationError(f"Firebase config file {v} does not exist")
        # This is a dictionary
        elif isinstance(v, dict):    
            config = v
        # This is neither a file path nor a dictionary
        else:   
            InvalidFirebaseConfigurationError("Firebase config must be a file path or a dictionary")

        # Initialize Firebase Admin
        firebase_admin.initialize_app(credentials.Certificate(config))

        return config
    
    @field_validator('import_users')
    def validate_import_users(cls, v):
        if not isinstance(v, bool):
            raise InvalidFirebaseConfigurationError("import_users must be a boolean")
        # If import_users is True, import users from Firebase
        if v:
            try:
                if check_table_exists("drf_easily_saas_firebaseuserinformations") and check_table_empty("drf_easily_saas_firebaseuserinformations"):
                    import_users()
            except Exception as e:
                raise InvalidFirebaseConfigurationError(f"Error importing users from Firebase: {str(e)}")
        return v

    @field_validator('hot_reload_import')
    def validate_hot_reload_import(cls, v):
        if not isinstance(v, bool):
            raise InvalidFirebaseConfigurationError("hot_reload_import must be a boolean")
        if v:
            try:
                if check_table_exists("drf_easily_saas_firebaseuserinformations") and not check_table_empty("drf_easily_saas_firebaseuserinformations"):
                    import_users()
                elif not check_table_exists("drf_easily_saas_firebaseuserinformations"):
                    return v
            except Exception as e:
                raise InvalidFirebaseConfigurationError(f"Error importing users from Firebase: {str(e)}")
        return v