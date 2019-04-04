
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool

from multiprocessing import cpu_count
from typing import List
import tqdm

from .scraper import getLocs

def getLocList(uniProtIDs: List, nThread: int = None) -> List:

    #calculate number of threads reqired
    _nThread = int(1)
    listLen = len(uniProtIDs)
    cpuCount = cpu_count()
    if nThread is None:
        _nThread = cpuCount if cpuCount < listLen else listLen
    else:
        assert(nThread <= cpuCount)
        _nThread = nThread

    #lookup locs using thread pool
    with Pool(processes=_nThread) as pool:
        ret = list(tqdm.tqdm(pool.imap(getLocs, uniProtIDs), total = listLen, miniters=1))

    return ret
