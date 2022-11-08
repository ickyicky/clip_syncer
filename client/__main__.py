from .clipboard_watcher import ClipboardContentWatcher
from .manager import ClipboardContentManager
from .connection import WebSocketConnection
import argparse
from queue import Queue
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("API_URL", type=str, help="server api url")
    parser.add_argument(
        "--watcher-interval", "-w", type=float, help="watcher interval", default=0.0
    )
    parser.add_argument(
        "--manager-timeout", "-m", type=float, help="manager timeout", default=0.01
    )
    parser.add_argument(
        "--connection-timeout",
        "-c",
        type=float,
        help="connection timeout",
        default=0.01,
    )
    parser.add_argument("--interval", "-i", type=float, help="interval", default=0.1)

    args = parser.parse_args()

    local_queue = Queue()
    remote_queue = Queue()

    watcher = ClipboardContentWatcher(local_queue, check_interval=args.watcher_interval)
    manager = ClipboardContentManager(
        remote_queue, watcher, timeout=args.manager_timeout
    )
    connection = WebSocketConnection(
        args.API_URL,
        remote_queue=remote_queue,
        local_queue=local_queue,
        timeout=args.connection_timeout,
    )

    threads = (watcher, manager, connection)

    for thread in threads:
        thread.start()

    try:
        while True:
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass

    for thread in threads:
        thread.stop()

    for thread in threads:
        thread.join()
