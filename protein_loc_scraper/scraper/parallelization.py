
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool

from multiprocessing import cpu_count
from typing import List
import tqdm
import sys

from .scraper import getLocs

def getLocList(uniProtIDs: List, nThread: int = None) -> List:
    '''
    Given a list of uniprot IDs, return a list in the same order containing uniprot
    annotations for subcellular localization.

    :param uniProtIDs: uniprot IDs of proteins to look up.
    :param nThread: Nunber of threads to use
    :param threadMult: Factor to multiply number of logical cores by to get number of threads to use.
    :return: List of subcellular locations.
    '''

    #calculate number of threads reqired
    _nThread = int(1)
    listLen = len(uniProtIDs)
    cpuCount = cpu_count()
    if nThread is None:
        _nThread = cpuCount if cpuCount < listLen else listLen
    else:
        _nThread = nThread

    #lookup locs using thread pool
    sys.stdout.write('Searching for locations with {} threads...\n'.format(_nThread))
    with Pool(processes=_nThread) as pool:
        ret = list(tqdm.tqdm(pool.imap(getLocs, uniProtIDs),
                             total = listLen,
                             miniters=1,
                             file = sys.stdout))

    return ret
