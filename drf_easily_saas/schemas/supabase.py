from supabase import create_client, Client
from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

# Drf Easily Saas
from drf_easily_saas.exceptions.supabase import InvalidSupabaseConfigurationError
from drf_easily_saas.utils.db import (
    check_table_exists, 
    check_table_empty
    )


# -------------------------------------------- #
# Supabase settings schema validation
# -------------------------------------------- #
class SupabaseConfig(BaseModel):
    """
    This class is used to validate the Supabase configuration.

    On this class, we validate the Supabase configuration and import users from Supabase if import_users is True.

    Args:
    - url (str): Supabase URL
    - anon_key (str): Supabase anonymous key
    - service_role_key (str): Supabase service role key
    - import_users (bool): Import users from Supabase
    - hot_reload_import (bool): Hot reload import users

    Returns:
    - url (str): Supabase URL
    - anon_key (str): Supabase anonymous key  
    - service_role_key (str): Supabase service role key
    - import_users (bool): Import users from Supabase
    - hot_reload_import (bool): Hot reload import users
    """
    url: str
    anon_key: str
    service_role_key: str
    import_users: bool
    hot_reload_import: bool = False
    
    @field_validator('url')
    def validate_url(cls, v):
        if not v:
            raise InvalidSupabaseConfigurationError("Supabase URL cannot be empty")
        if not v.startswith('https://'):
            raise InvalidSupabaseConfigurationError("Supabase URL must start with https://")
        if not v.endswith('.supabase.co'):
            raise InvalidSupabaseConfigurationError("Supabase URL must end with .supabase.co")
        return v
    
    @field_validator('anon_key')
    def validate_anon_key(cls, v):
        if not v:
            raise InvalidSupabaseConfigurationError("Supabase anon key cannot be empty")
        return v
        
    @field_validator('service_role_key')
    def validate_service_role_key(cls, v):
        if not v:
            raise InvalidSupabaseConfigurationError("Supabase service role key cannot be empty")
        return v
    
    @field_validator('import_users')
    def validate_import_users(cls, v):
        if not isinstance(v, bool):
            raise InvalidSupabaseConfigurationError("import_users must be a boolean")
        # If import_users is True, import users from Supabase
        if v:
            try:
                if check_table_exists("drf_easily_saas_supabaseuserinformations") and check_table_empty("drf_easily_saas_supabaseuserinformations"):
                    # Import at runtime to avoid circular imports
                    from drf_easily_saas.auth.supabase.protect import import_users
                    import_users()
            except Exception as e:
                raise InvalidSupabaseConfigurationError(f"Error importing users from Supabase: {str(e)}")
        return v

    @field_validator('hot_reload_import')
    def validate_hot_reload_import(cls, v):
        if not isinstance(v, bool):
            raise InvalidSupabaseConfigurationError("hot_reload_import must be a boolean")
        if v:
            try:
                if check_table_exists("drf_easily_saas_supabaseuserinformations") and not check_table_empty("drf_easily_saas_supabaseuserinformations"):
                    # Import at runtime to avoid circular imports
                    from drf_easily_saas.auth.supabase.protect import import_users
                    import_users()
                elif not check_table_exists("drf_easily_saas_supabaseuserinformations"):
                    return v
            except Exception as e:
                raise InvalidSupabaseConfigurationError(f"Error importing users from Supabase: {str(e)}")
        return v