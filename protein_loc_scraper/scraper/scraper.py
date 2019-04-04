
import requests
from typing import List
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
    ret = [x for x in locList if x not in SKIP_LOCS]
    ret = removeDuplicates(ret)
    if not ret:
        return 'no_annotated_location'
    return delim.join(ret)


def getLocs(uniprotID: str) -> str:
    url = 'http://www.uniprot.org/uniprot/' + uniprotID + '.html'
    response = requests.get(url)
    if response.status_code >= 400:
        return "No_uniprot_records_found"

    tree = html.fromstring(response.content)
    sl = tree.xpath('//*[@id="table-uniprot_annotation"]/div/ul/li/h6/text()')
    ssl = tree.xpath('//*[@id="table-uniprot_annotation"]/div/ul/li/ul/li/a/text()')
    locs = _concatLocs([x.lower().strip() for x in sl + ssl])

    return locs

