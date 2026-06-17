import requests
from urllib.parse import urlparse

###
## Check the URL format is correctly 
###
@staticmethod
def _is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

####
## Check the protocol too add url
###
@staticmethod
def _check_protocol(url:str)-> str:
    try:
        requests.get(url=f"https://{url}",timeout=5)
        return "https://"
    except requests.exceptions.RequestException:
        try:
            requests.get(url=f"http://{url}",timeout=5)
            return "http://"
        except requests.exceptions.RequestException:
            return None
###
## Return the corretly URL 
###
@staticmethod
def return_clear_URL(url: str) -> str | None:
    url = str(url).strip()
    if not isinstance(url, str):
        return None
    
    if _is_valid_url(url):
        return url
    protocol = _check_protocol(url)
    if protocol is not None:
        url = url.strip()
        return protocol + url
    else:
        return None
