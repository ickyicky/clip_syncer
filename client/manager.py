import pyperclip
from queue import Queue, Empty
from typing import Union
from .base import StoppableThread
from .clipboard_watcher import ClipboardContentWatcher


class ClipboardContentManager(StoppableThread):
    """
    ClipboardContentManager pastes new content
    from remote server and tells Watcher to ignore it
    so its not broadcasted
    """

    def __init__(
        self,
        queue: Queue,
        watcher: ClipboardContentWatcher,
        timeout: Union[int, float] = 0.01,
    ):
        super().__init__()
        self.queue = queue
        self.watcher = watcher
        self.timeout = timeout

    def run(self) -> None:
        while not self.stopped():
            try:
                content = self.queue.get(timeout=self.timeout)
            except Empty:
                continue

            if content is not None:
                self.watcher.set_ignore(content)
                pyperclip.copy(content)
