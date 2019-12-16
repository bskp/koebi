#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run an OSC server with asynchroneous I/O handling via the uasync framwork."""

import sys
import logging
import socket
import gc

from uasyncio.core import IORead, coroutine, get_event_loop, sleep

if __debug__:
    from uosc.socketutil import get_hostport
from uosc.server import handle_osc

MAX_DGRAM_SIZE = 500
log = logging.getLogger("uosc.async_server")


def run_server(host, port, client_coro, **params):
    if __debug__: log.debug("run_server(%s, %s)", host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    try:
        while True:
            if __debug__: log.debug("run_server: Before IORead")
            yield IORead(sock)
            if __debug__: log.debug("run_server: Before recvfrom")
            data, caddr = sock.recvfrom(MAX_DGRAM_SIZE)
            if __debug__: log.debug("RECV %i bytes from %s:%s",
                                    len(data), *get_hostport(caddr))
            yield client_coro(data, caddr, **params)
    finally:
        sock.close()
        log.info("Bye!")
        gc.mem_free()


@coroutine
def serve(data, caddr, **params):
    if __debug__: log.debug("Client request handler coroutine called.")
    handle_osc(data, caddr, **params)
    if __debug__: log.debug("Finished processing request,")
