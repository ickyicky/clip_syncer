# Clipboard synchronization

Simple python application that allows for clipboard syncrhonization across multiple devices.

## Usage

Install requirements:

```bash
pip3 install -r requirements.txt
```

The application requires setting up server that allows all clients to communicate. Splin it up with:

```bash
uvicorn server:app
```

Then connect all clinets with:

```bash
python3 -m client ws://127.0.0.1:8000/pubsub http://127.0.0.1:8000/publish
```
