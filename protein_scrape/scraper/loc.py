
from typing import List, Tuple
from lxml import html

from .parallelization import scrape
from .utils import _make_request, removeDuplicates
from .constants import SL_XPATH, SSL_XPATH, GO_XPATH, SGO_XPATH, REQUEST_ERROR, UNIPROT_ERROR

SKIP_LOCS = ['other locations']


def getLocList(uniprotIDs: List, nThread: int = None) -> List:
    return scrape(uniprotIDs, getLocs, nThread)


def _concatLocs(locList: List, delim: str = ';') -> str:
    #process text and remove any string in SKIP_LOCS
    ret = list(filter(lambda x: x not in SKIP_LOCS, [y.lower().strip() for y in locList]))
    ret = removeDuplicates(ret)
    if not ret:
        return 'no_annotated_location'
    return delim.join(ret)


def getLocs(uniprotID: str, nRetry: int = 10) -> Tuple:
    RETURN_COUNT = 3
    response = _make_request(uniprotID, nRetry)

    if response is None:
        return tuple(REQUEST_ERROR for _ in range(RETURN_COUNT))

    if response.status_code >= 400:
        return tuple(UNIPROT_ERROR for _ in range(RETURN_COUNT))

    tree = html.fromstring(response.content)

    #get sl uniprot anotation
    sl = tree.xpath(SL_XPATH)
    ssl = tree.xpath(SSL_XPATH)
    locs = _concatLocs(sl + ssl)

    #get go term for celluar component
    go = tree.xpath(GO_XPATH)
    sgo = tree.xpath(SGO_XPATH)
    gos = _concatLocs(go + sgo)

    concat = _concatLocs(sl + ssl + go + sgo)

    return locs, gos, concat

