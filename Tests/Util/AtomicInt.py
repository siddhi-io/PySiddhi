from multiprocessing import RLock


class AtomicInt:
    '''
    An atomic integer class. All operations are thread safe.
    '''

    def __init__(self, value=0):
        self.value = value
        self.lock = RLock()

    def set(self, value):
        self.lock.acquire()
        self.value = value
        self.lock.release()

    def addAndGet(self, value):
        self.lock.acquire()
        self.value += value
        val = self.value
        self.lock.release()
        return val
    def get(self):
        self.lock.acquire()
        val = self.value
        self.lock.release()
        return val

