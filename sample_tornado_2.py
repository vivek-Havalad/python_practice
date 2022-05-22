import time
import threading
import multiprocessing
import math

from tornado.web import RequestHandler, Application, asynchronous
from tornado.ioloop import IOLoop


# run in some other process - put result in q
def heavy_lifting(q):
    t0 = time.time()
    for k in range(2000):
        math.factorial(k)

    t = time.time()
    q.put(t - t0)  # report time to compute in queue


class FastHandler(RequestHandler):
    def get(self):
        res = 'fast result ' + self.get_argument('id')
        print res
        self.write(res)
        self.flush()


class MultiThreadedHandler(RequestHandler):
    # Note:  This handler can be called with threaded = True or False
    def initialize(self, threaded=True):
        self._threaded = threaded
        self._q = multiprocessing.Queue()

    def start_process(self, worker, callback):
        # method to start process and watcher thread
        self._callback = callback

        if self._threaded:
            # launch process
            multiprocessing.Process(target=worker, args=(self._q,)).start()

            # start watching for process to finish
            threading.Thread(target=self._watcher).start()

        else:
            # threaded = False just call directly and block
            worker(self._q)
            self._watcher()

    def _watcher(self):
        # watches the queue for process result
        while self._q.empty():
            time.sleep(0)  # relinquish control if not ready

        # put callback back into the ioloop so we can finish request
        response = self._q.get(False)
        IOLoop.instance().add_callback(lambda: self._callback(response))


class SlowHandler(MultiThreadedHandler):
    @asynchronous
    def get(self):
        # start a thread to watch for
        self.start_process(heavy_lifting, self._on_response)

    def _on_response(self, delta):
        _id = self.get_argument('id')
        res = 'slow result {} <--- {:0.3f} s'.format(_id, delta)
        print res
        self.write(res)
        self.flush()
        self.finish()   # be sure to finish request


application = Application([
    (r"/fast", FastHandler),
    (r"/slow", SlowHandler, dict(threaded=False)),
    (r"/slow_threaded", SlowHandler, dict(threaded=True)),
])


if __name__ == "__main__":
    application.listen(8888)
    IOLoop.instance().start()
