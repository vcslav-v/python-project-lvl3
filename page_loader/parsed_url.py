def add_scheme(url: str) -> str:
    if '://' not in url:
        return 'http://' + url
    return url
