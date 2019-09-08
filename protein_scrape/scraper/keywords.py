
from typing import Tuple, List
from lxml import html

from .parallelization import scrape
from .utils import _make_request
from .constants import FXN_PATH, LIGAND_PATH, REQUEST_ERROR, UNIPROT_ERROR


def getFxnList(uniprotIDs: List, nThread: int = None) -> List:
    return scrape(uniprotIDs, getFxn, nThread)


def _concatFxn(fxnList: List, delim: str = ';') -> str:
    ret = delim.join(fxnList)
    if not ret:
        return 'no_annotation'
    return ret


def getFxn(uniprotID: str, nRetry: int = 10) -> Tuple:
    RETURN_COUNT = 3
    response = _make_request(uniprotID, nRetry)

    if response is None:
        return tuple(REQUEST_ERROR for _ in range(RETURN_COUNT))

    if response.status_code >= 400:
        return tuple(UNIPROT_ERROR for _ in range(RETURN_COUNT))

    tree = html.fromstring(response.content)

    #get fxn and ligand
    fxn = tree.xpath(FXN_PATH)
    ligand = tree.xpath(LIGAND_PATH)

    #concat lists
    fxns = _concatFxn(fxn)
    ligands = _concatFxn(ligand)
    concat = _concatFxn(fxn + ligand)

    return fxns, ligands, concat



