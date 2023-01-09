
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool

from multiprocessing import cpu_count
from typing import List
from tqdm import tqdm
import sys

def scrape(uniProtIDs: List, scrapeFunction, nThread: int = None, verbose: bool = False) -> List:
    '''
    Given a list of uniprot IDs, return a list in the same order containing uniprot
    annotations for subcellular localization.

    :param scrapeFunction a function that takes a single uniprot id and returns a string or tuple.
    :param uniProtIDs: uniprot IDs of proteins to look up.
    :param nThread: Number of threads to use
    :param verbose: If true, print verbose output when making requests.
    :return: List of subcellular locations.
    '''

    #calculate number of threads required
    _nThread = int(1)
    listLen = len(uniProtIDs)
    cpuCount = cpu_count()
    if nThread is None:
        _nThread = cpuCount if cpuCount < listLen else listLen
    else:
        _nThread = nThread

    #lookup locs using thread pool
    sys.stdout.write('Searching for data with {} thread(s)...\n'.format(_nThread))
    if _nThread == 1 and verbose:
        ret = list()
        for i, protein in enumerate(uniProtIDs):
            ret.append(scrapeFunction(protein))
            sys.stdout.write(f'Working on {i} of {len(uniProtIDs)}...\r')
            sys.stdout.flush()
        sys.stdout.write(' Done!\n')
    else:
        with Pool(processes=_nThread) as pool:
            ret = list(tqdm(pool.imap(scrapeFunction, uniProtIDs),
                            total = listLen,
                            miniters=1,
                            file = sys.stdout))

    return ret

