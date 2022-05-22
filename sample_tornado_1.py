import time
from functools import wraps
from multiprocessing.pool import Pool

import tornado.web
from tornado import gen
from tornado.gen import Return
from tornado import stack_context
from tornado.ioloop import IOLoop
from tornado.concurrent import Future

def _argument_adapter(callback):
    def wrapper(*args, **kwargs):
        if kwargs or len(args) > 1:
            callback(Arguments(args, kwargs))
        elif args:
            callback(args[0])
        else:
            callback(None)
    return wrapper

def PoolTask(func, *args, **kwargs):
    """ Task function for use with multiprocessing.Pool methods.

    This is very similar to tornado.gen.Task, except it sets the
    error_callback kwarg in addition to the callback kwarg. This
    way exceptions raised in pool worker methods get raised in the
    parent when the Task is yielded from.

    """
    future = Future()
    def handle_exception(typ, value, tb):
        if future.done():
            return False
        future.set_exc_info((typ, value, tb))
        return True
    def set_result(result):
        if future.done():
            return
        if isinstance(result, Exception):
            future.set_exception(result)
        else:
            future.set_result(result)
    with stack_context.ExceptionStackContext(handle_exception):
        cb = _argument_adapter(set_result)
        func(*args, callback=cb, error_callback=cb)
    return future

def coro_runner(func):
    """ Wraps the given func in a PoolTask and returns it. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return PoolTask(func, *args, **kwargs)
    return wrapper

class MetaPool(type):
    """ Wrap all *_async methods in Pool with coro_runner. """
    def __new__(cls, clsname, bases, dct):
        pdct = bases[0].__dict__
        for attr in pdct:
            if attr.endswith("async") and not attr.startswith('_'):
                setattr(bases[0], attr, coro_runner(pdct[attr]))
        return super().__new__(cls, clsname, bases, dct)

class TornadoPool(Pool, metaclass=MetaPool):
    pass

# Test worker functions
def test2(x):
    print("hi2")
    raise Exception("eeee")

def test(x):
    print(x)
    time.sleep(2)
    return "done"

class TestHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            result = yield pool.apply_async(test, ("inside get",))
            self.write("%s\n" % result)
            result = yield pool.apply_async(test2, ("hi2",))
            self.write("%s\n" % result)
        except Exception as e:
            print("caught exception in get")
            self.write("Caught an exception: %s" % e)
            raise
        finally:
            self.finish()

app = tornado.web.Application([
    (r"/test", TestHandler),
])

if __name__ == "__main__":
    pool = TornadoPool()
    app.listen(8888)
    IOLoop.instance().start()
