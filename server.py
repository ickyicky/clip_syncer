from fastapi import FastAPI
from fastapi_websocket_pubsub import PubSubEndpoint
from pydantic import BaseModel


app = FastAPI()

endpoint = PubSubEndpoint()
endpoint.register_route(app, "/pubsub")


class Event(BaseModel):
    time: float
    content: str


@app.post("/publish")
async def publish(event: Event):
    await endpoint.publish(["event"], data=[event.content, event.time])
