from drf_easily_saas.exceptions.base import EasilySaasError


# --------------------------------------------------------- #
# Exceptions for the configuration of the package
# --------------------------------------------------------- #

class InvalidConfigurationError(EasilySaasError):
    """Exception raised for errors in the configuration of the package."""
    def __init__(self, message="Invalid configuration provided"):
        self.message = message
        super().__init__(self.message)

class InvalidPaymentConfigurationError(EasilySaasError):
    """Exception raised for errors in the payment configuration of the package."""
    def __init__(self, message="Invalid payment configuration provided"):
        self.message = message
        super().__init__(self.message)

class InvalidAuthConfigurationError(EasilySaasError):
    """Exception raised for errors in the authentication configuration of the package."""
    def __init__(self, message="Invalid authentication configuration provided"):
        self.message = message
        super().__init__(self.message)

class InvalidFrontendUrlError(EasilySaasError):
    """Exception raised for errors in the frontend url configuration of the package."""
    def __init__(self, message="Invalid frontend url provided"):
        self.message = message
        super().__init__(self.message)


    