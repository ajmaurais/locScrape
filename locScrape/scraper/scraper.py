
import requests
import sys
from typing import List, Tuple
from lxml import html

SKIP_LOCS = ['other locations']

def removeDuplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def _concatLocs(locList: List, delim: str = ';') -> str:
    #process text and remove any string in SKIP_LOCS
    ret = list(filter(lambda x: x not in SKIP_LOCS, [y.lower().strip() for y in locList]))
    ret = removeDuplicates(ret)
    if not ret:
        return 'no_annotated_location'
    return delim.join(ret)


def getLocs(uniprotID: str, nRetry: int = 10) -> Tuple:
    url = 'http://www.uniprot.org/uniprot/' + uniprotID + '.html'
    response = None
    for i in range(nRetry):
        try:
            response = requests.get(url)
        except(requests.exceptions.ConnectionError,
               requests.exceptions.ChunkedEncodingError):
            sys.stderr.write('Retry {} of {} for {}\n'.format(i, nRetry, uniprotID))
            continue
        else:
            break

    if response is None:
        return 'error_getting_page', 'error_getting_page', 'error_getting_page'

    if response.status_code >= 400:
        return 'no_uniprot_records_found', 'no_uniprot_records_found', 'no_uniprot_records_found'

    tree = html.fromstring(response.content)

    #get sl uniprot anotation
    sl = tree.xpath('//*[@id="table-uniprot_annotation"]/div/ul/li/h6/text()')
    ssl = tree.xpath('//*[@id="table-uniprot_annotation"]/div/ul/li/ul/li/a/text()')
    locs = _concatLocs(sl + ssl)

    #get go term for celluar component
    go = tree.xpath('//*[@id="table-go_annotation"]/div/ul/li/h6/text()')
    sgo = tree.xpath('//*[@id="table-go_annotation"]/div/ul/li/ul/li/a/text()')
    gos = _concatLocs(go + sgo)

    concat = _concatLocs(sl + ssl + go + sgo)

    return locs, gos, concat

