
import requests
import sys

from .constants import UNIPROT_URL


def _make_request(uniprotID: str, nRetry: int = 10):

    url = UNIPROT_URL + uniprotID + '.xml'
    n_iter = nRetry if nRetry > 0 else 1
    response = None
    for i in range(n_iter):
        try:
            response = requests.get(url)
            return response
        except(requests.exceptions.ConnectionError,
               requests.exceptions.ChunkedEncodingError):
            sys.stderr.write('Retry {} of {} for {}\n'.format(i, nRetry, uniprotID))
            continue

