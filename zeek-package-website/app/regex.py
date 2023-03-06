import re


def standardize_tag(in_tag: str) -> str:

    out_tag = re.sub("([i][n][g]$)|([s]$)", "", in_tag.strip())

    return re.sub("([ -])", "_", out_tag)


def search(in_query: str) -> []:

    pass
