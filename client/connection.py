from fastapi_websocket_pubsub import PubSubClient
from queue import Queue
import asyncio
import requests
from typing import Union
from .base import StoppableThread
from .event import NewKeyboardContent


class WebSocketConnection(StoppableThread):
    def __init__(
        self,
        api_url: str,
        remote_queue: Queue,
        timeout: Union[int, float] = 0.01,
    ):
        super().__init__()
        self.api_url = api_url
        self.remote_queue = remote_queue
        self.timeout = timeout
        self.loop = asyncio.BaseEventLoop()

    def run(self):
        asyncio.run(self.main())

    async def on_events(self, data, topic):
        print(f"RECEIVED: {data}")
        self.remote_queue.put(NewKeyboardContent(time=data[1], content=data[0]))

    async def stop_client(self):
        while not self.stopped():
            await asyncio.sleep(self.timeout)

        await self.client.disconnect()

    async def main(self):
        self.client = PubSubClient(["event"], callback=self.on_events)
        self.client.start_client(self.api_url)
        await self.stop_client()
        await self.client.wait_until_done()
