import websocket
import time
import rel
from queue import Queue, Empty
from typing import Union
from .base import StoppableThread
from .event import NewKeyboardContent


class WebSocketConnection(StoppableThread):
    def __init__(
        self,
        api_url: str,
        remote_queue: Queue,
        local_queue: Queue,
        timeout: Union[int, float] = 0.01,
    ):
        super().__init__()
        self.websocket = websocket.WebSocketApp(
            api_url,
            on_message=self.handle_new_content,
        )
        self.websocket.run_forever(dispatcher=rel)
        self.remote_queue = remote_queue
        self.local_queue = local_queue
        self.timeout = timeout

    def handle_new_content(self, ws, content: str) -> None:
        print(f"RECEIVED: {content}")
        self.remote_queue.put(NewKeyboardContent(time=time.time(), content=content))

    def run(self):
        while not self.stopped():
            try:
                content = self.local_queue.get(timeout=self.timeout)
            except Empty:
                continue

            if content is not None:
                self.websocket.send(content.content)
                print(f"SEND: {content.content}")

        rel.signal(2, rel.abort)
        rel.dispatch()
