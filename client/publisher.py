from .base import StoppableThread
import requests
from typing import Union
from queue import Queue


class Publisher(StoppableThread):
    def __init__(
        self, api_url: str, local_queue: Queue, interval: Union[int, float] = 0.01
    ):
        super().__init__()
        self.api_url = api_url
        self.local_queue = local_queue

    def run(self) -> None:
        while not self.stopped():
            if not self.local_queue.empty():
                item = self.local_queue.get()
                if item is None:
                    continue
                requests.post(
                    self.api_url,
                    json={"time": item.time, "content": item.content},
                )
