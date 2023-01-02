
import requests
import sys

from .constants import UNIPROT_URL


def removeDuplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def _make_request(uniprotID: str, nRetry: int = 10):

    url = UNIPROT_URL + uniprotID + '.html'
    n_iter = nRetry if nRetry > 0 else 1
    response = None
    for i in range(n_iter):
        try:
            response = requests.get(url)
        except(requests.exceptions.ConnectionError,
               requests.exceptions.ChunkedEncodingError):
            sys.stderr.write('Retry {} of {} for {}\n'.format(i, nRetry, uniprotID))
            continue

    return response
