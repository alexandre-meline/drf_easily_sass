from drf_easily_saas.exceptions.config import InvalidConfigurationError
from drf_easily_saas.exceptions.base import EasilySaasError


class InvalidStripeConfigurationError(InvalidConfigurationError):
    """Exception raised for errors during the Stripe configuration."""
    def __init__(self, message="Invalid Stripe configuration"):
        self.message = message
        super().__init__(self.message)

class StripePaymentProcessingError(EasilySaasError):
    """Exception raised for errors during the Stripe payment processing."""
    def __init__(self, message="Invalid Stripe payment processing"):
        self.message = message
        super().__init__(self.message)