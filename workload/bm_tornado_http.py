
"""Test the performance of simple HTTP serving and client using the Tornado
framework.

A trivial "application" is generated which generates a number of chunks of
data as a HTTP response's body.
"""

# import gc_count_module
import time
import sys
import socket


from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets
from tornado.web import RequestHandler, Application


HOST = "127.0.0.1"
FAMILY = socket.AF_INET

CHUNK = b"Hello world\n" * 1000
NCHUNKS = 1000

CONCURRENCY = 150


class MainHandler(RequestHandler):

    @coroutine
    def get(self):
        # for i in range(NCHUNKS):
        #     self.write(CHUNK)
        #     yield self.flush()
        self.write(CHUNK * NCHUNKS)

    def compute_etag(self):
        # Overriden to avoid stressing hashlib in this benchmark
        return None


def make_application():
    return Application([
        (r"/", MainHandler),
    ])


def make_http_server(request_handler):
    server = HTTPServer(request_handler)
    sockets = bind_sockets(0, HOST, family=FAMILY)
    assert len(sockets) == 1
    server.add_sockets(sockets)
    sock = sockets[0]
    return server, sock


def bench_tornado(loops):
    server, sock = make_http_server(make_application())
    host, port = sock.getsockname()
    url = "http://%s:%s/" % (host, port)

    @coroutine
    def run_client():
        client = AsyncHTTPClient()
        range_it = range(loops)

        for _ in range_it:
            futures = [client.fetch(url) for j in range(CONCURRENCY)]
            for fut in futures:
                resp = yield fut
                buf = resp.buffer
                buf.seek(0, 2)
                assert buf.tell() == len(CHUNK) * NCHUNKS

        client.close()

    IOLoop.current().run_sync(run_client)
    server.stop()


if __name__ == "__main__":
    # 3.8 changed the default event loop to ProactorEventLoop which doesn't
    # implement everything required by tornado and breaks this benchmark.
    # Restore the old WindowsSelectorEventLoop default for now.
    # https://bugs.python.org/issue37373
    # https://github.com/python/pyperformance/issues/61
    # https://github.com/tornadoweb/tornado/pull/2686
    start_time = time.time()
    # gc_count_module.start_count_gc_list(
    #     250_000, "obj_dump.txt", 1, 10, 1_000_000)
    bench_tornado(15)
    # gc_count_module.close_count_gc_list()
    add_time = time.time() - start_time
    print(f"Compute time: {add_time:.2f} seconds", file=sys.stderr)
