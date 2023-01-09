
from typing import List, Tuple
from lxml import html

from .parallelization import scrape
from .utils import _make_request
from .constants import SL_XPATH, GO_XPATH, REQUEST_ERROR, UNIPROT_ERROR, CELLULAR_COMPONENT_RE

SKIP_LOCS = ['other locations']


def getLocList(uniprotIDs: List, **kwargs) -> List:
    return scrape(uniprotIDs, getLocs, **kwargs)


def _concatLocs(locList: List, delim: str = ';') -> str:
    #process text and remove any string in SKIP_LOCS
    ret = list(set(filter(lambda x: x not in SKIP_LOCS, [y.lower().strip() for y in locList])))
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
    # ssl = tree.xpath(SSL_XPATH)
    # locs = _concatLocs(sl + ssl)
    locs = _concatLocs(sl)

    #get go term for celluar component
    go = tree.xpath(GO_XPATH)
    # sgo = tree.xpath(SGO_XPATH)
    # gos = _concatLocs(go + sgo)
    gos = _concatLocs([CELLULAR_COMPONENT_RE.sub('', x) for x in go if CELLULAR_COMPONENT_RE.search(x)])

    concat = _concatLocs(sl + gos)

    return locs, gos, concat

