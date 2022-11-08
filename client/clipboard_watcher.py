import pyperclip
import time
from typing import Union, Optional
from queue import Queue
from .base import StoppableThread
from .event import NewKeyboardContent


class ClipboardContentWatcher(StoppableThread):
    """
    ClipboardContentWatcher watches for new clipboard content
    and pushes it into desired queue. Each event is stamped with
    current time. It's configured with cliboard checking interval
    """

    def __init__(self, queue: Queue, check_interval: Union[int, float] = 0.01):
        super().__init__()
        self.queue = queue
        self.check_interval = check_interval
        self.current_content = None
        self._ignore_content = Queue()

    def set_ignore(self, content: str):
        """
        Tells to ignore next content
        """
        self._ignore_content.put(content)

    def ignored_content(self) -> Optional[str]:
        if not self._ignore_content.empty():
            return self._ignore_content.get()

    def run(self) -> None:
        while not self.stopped():
            current_content = pyperclip.paste()
            ignored_content = self.ignored_content()

            if (
                current_content != self.current_content
                and current_content != ignored_content
            ):
                self.current_content = current_content
                self.queue.put(
                    NewKeyboardContent(time=time.time(), content=self.current_content)
                )

            time.sleep(self.check_interval)
