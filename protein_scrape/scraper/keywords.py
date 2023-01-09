
from typing import Dict, List
from lxml import html

from .parallelization import scrape
from .utils import _make_request
from .constants import REQUEST_ERROR, UNIPROT_ERROR, ERROR_HEADER


def getFxnList(uniprotIDs: List, nThread: int = None) -> List:
    return scrape(uniprotIDs, getFxn, nThread)


def _concatFxn(fxnList: List, delim: str = ';') -> str:
    ret = delim.join(fxnList)
    if not ret:
        return 'no_annotation'
    return ret


def getFxn(uniprotID: str, nRetry: int = 10) -> Dict:
    response = _make_request(uniprotID, nRetry)

    if response is None:
        return {ERROR_HEADER:REQUEST_ERROR}

    if response.status_code >= 400:
        return {ERROR_HEADER:UNIPROT_ERROR}

    tree = html.fromstring(response.content)

    headers = tree.xpath(KEYWORD_HEADER_PATH)

    ret = dict()
    for i, v in enumerate(headers):
        dat = tree.xpath(BASE_KEYWORD_DAT_PATH.format(i+1))
        ret[v] = _concatFxn(dat)

    return ret
