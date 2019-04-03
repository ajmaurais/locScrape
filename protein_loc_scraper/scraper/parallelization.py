
#from multiprocessing import Queue
#from multiprocessing import Process as Worker

from queue import Queue
from threading import Thread as Worker

from multiprocessing import cpu_count
from typing import List
import sys
import time

from .atomic_integer import AtomicCounter
from .scraper import getLocs

def progressBar(progress, barWidth = 50):

    sys.stdout.write('[')
    pos = int(barWidth * progress)

    for i in range(barWidth):
        if i < pos:
            sys.stdout.write('=')
        elif i == pos:
            sys.stdout.write('>')
        else: sys.stdout.write(' ')

    sys.stdout.write('] {}%\r'.format(int(progress * 100)))
    sys.stdout.flush()


def _getID_progress(counter: AtomicCounter, total: int,
                    sleepTime: float = 1, barWidth: int = 100):

    count = counter.values
    while(qsize < total):
        qsize = queue.qsize()
        time.sleep(sleepTime)
        progressBar(qsize, barWidth)


def _getID_helper(input_queue: Queue, output_queue: Queue, counter: AtomicCounter):
    while True:
        if input_queue.empty():
            break
        item = input_queue.get()
        output_queue.put((item, getLocs(item)))
        counter.increment(1)


def getLocList(uniProtIDs: List, nThread: int = None) -> List:
    #calculate number of threads reqired
    _nThread = int()
    listLen = len(uniProtIDs)
    cpuCount = cpu_count()
    if nThread is None:
        _nThread = cpuCount if cpuCount < listLen else listLen
    else:
        assert(nThread <= cpuCount)
        _nThread = nThread

    input_queue = Queue()
    output_queue = Queue()
    for id in uniProtIDs:
        input_queue.put(id)

    counter = AtomicCounter(0)
    workers = [Worker(target=_getID_helper, args = (input_queue, output_queue)) for _ in range(_nThread)]

    #start progress function
    workers.append(Worker(target=_getID_progress, args = (output_queue, listLen)))

    for t in workers:
        t.start()

    for t in workers:
        t.join()

    ret = list()
    while not output_queue.empty():
        result = output_queue.get()
        ret.append(result)

    return ret
