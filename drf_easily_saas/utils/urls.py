from urllib.parse import urlparse

# Exceptions
from drf_easily_saas.exceptions.base import ValidationError


def remove_last_slash(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        if parsed_url.path.endswith('/'):
            return url[:-1]
    except Exception as e:
        raise ValidationError(f"Error removing last slash from URL: {str(e)}")
    return url

def concat_urls(url1: str, url2: str) -> str:
    url1 = remove_last_slash(url1)
    url2 = remove_last_slash(url2)
    return url1 + url2