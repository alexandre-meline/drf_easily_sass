from drf_easily_saas.exceptions.config import InvalidConfigurationError


class InvalidSupabaseConfigurationError(InvalidConfigurationError):
    """Exception raised for errors during the Supabase configuration."""
    def __init__(self, message="Invalid Supabase configuration"):
        self.message = message
        super().__init__(self.message)