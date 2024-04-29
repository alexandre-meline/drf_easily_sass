from drf_easily_saas.exceptions.config import InvalidConfigurationError


class InvalidFirebaseConfigurationError(InvalidConfigurationError):
    """Exception raised for errors during the Firebase configuration."""
    def __init__(self, message="Invalid Firebase configuration"):
        self.message = message
        super().__init__(self.message)