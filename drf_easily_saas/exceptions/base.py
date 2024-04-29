# --------------------------------------------------------- #
# Exception classes for drf_easily_saas
# --------------------------------------------------------- #
class EasilySaasError(Exception):
    """Base class for other exceptions in drf_easily_saas."""
    pass

class DatabaseError(EasilySaasError):
    """Exception raised for errors during the database process."""
    def __init__(self, message="Database error"):
        self.message = message
        super().__init__(self.message)

class ValidationError(EasilySaasError):
    """Exception raised for errors during the validation process."""
    def __init__(self, message="Validation error"):
        self.message = message
        super().__init__(self.message)