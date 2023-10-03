#!/usr/bin/python
# -*- coding: UTF-8 -*-

import zmq
from constanstes import PROXY_CANAL


def main():

    context = zmq.Context()

    # Socket facing producers
    frontend = context.socket(zmq.XPUB)
    frontend.bind(f"tcp://*:{PROXY_CANAL['subscribers']}")

    # Socket facing consumers
    backend = context.socket(zmq.XSUB)
    backend.bind(f"tcp://*:{PROXY_CANAL['publishers']}")

    zmq.proxy(frontend, backend)

    # We never get here…
    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    main()