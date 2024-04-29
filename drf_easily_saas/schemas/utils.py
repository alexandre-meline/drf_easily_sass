from typing import Union

# Drf Easily Saas
from drf_easily_saas.schemas.config import EasilyConfig
from drf_easily_saas.exceptions.base import ValidationError
from drf_easily_saas.exceptions.config import InvalidConfigurationError


def validate_settings(settings_dict) -> Union[EasilyConfig, None]:
    try:
        config = EasilyConfig(**settings_dict)
        return config
    except ValidationError as e:
        raise InvalidConfigurationError(e.json())