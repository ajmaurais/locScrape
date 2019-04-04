
from typing import Dict
import csv

class DataFrame(object):

    _ROW_NAME = '_row'

    def __init__(self, data: Dict = None):
        self.nrow = 0
        self.ncol = 0
        self.data = dict()
        self.columns = list()

        if not data is None:
            self._fromDict(data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def _fromDict(self, data: Dict):
        for i, k, v in enumerate(data.items()):
            if i == 0:
                self.nrow = len(v)
            else:
                if self.nrow != len(v):
                    raise ValueError('Columns must all be same length!')
            self.data[k] = v
            self.columns.append(k)
        self.ncol = len(self.columns)
        self.data[DataFrame._ROW_NAME] = [x for x in range(self.nrow)]


    def iterrows(self):
        for i, _ in enumerate(self.data[DataFrame._ROW_NAME]):
            if i < self.nrow:
                yield i, {col:self.data[col][i] for col in self.data.keys()}
            else:
                raise StopIteration()


    def to_csv(self, ofname: str, sep: str = '\t'):
        outF = open(ofname, 'w')

        #print headers
        for i, s in enumerate(self.columns):
            if i == 0:
                outF.write('{}'.format(s))
            else: outF.write('\t{}'.format(s))
        outF.write('\n')

        for i, row in self.iterrows():
            for col in self.columns:
                if i == 0:
                    outF.write('{}'.format(row[col]))
                else: outF.write('\t{}'.format(row[col]))
            outF.write('\n')


def read_tsv(fname: str, hasHeader: bool = True):
    inF = open(fname, 'r')
    lines = inF.read().splitlines()
    delim = csv.Sniffer().sniff(lines[0]).delimiter
    ret = DataFrame()

    #add row keys
    _keys = dict()
    if hasHeader:
        _keys = [x.strip() for x in lines[0].split(delim)]
        _start = 1
    else:
        _keys = [x for x in range(len(lines[0].split(delim)))]
        _start = 0
    ret.data = {x: list() for x in _keys}
    ret.data[DataFrame._ROW_NAME] = list()
    ret.columns = _keys
    ret.ncol = len(_keys)

    #iterate through lines
    for i, line in enumerate(lines[_start:]):
        elems = [x.strip() for x in line.split(delim)]
        if len(elems) != ret.ncol:
            raise RuntimeError('Incorect number elements in row: {}'.format(i))
        for j, elem in enumerate(elems):
            ret.data[ret.columns[j]].append(elem)
        ret.data[DataFrame._ROW_NAME].append(i)
    ret.nrow = len(ret.data[DataFrame._ROW_NAME])

    return ret

