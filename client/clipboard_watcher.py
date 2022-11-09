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
        self.last_update_time = time.time()
        self._ignore_content = Queue()

    def set_ignore(self, content: NewKeyboardContent):
        """
        Tells to ignore next content
        """
        self._ignore_content.put(content)

    def ignored_content(self) -> Optional[NewKeyboardContent]:
        if not self._ignore_content.empty():
            return self._ignore_content.get()

    def run(self) -> None:
        ignored_content = None
        while not self.stopped():
            current_content = pyperclip.paste()
            ignored_content = self.ignored_content() or ignored_content

            if current_content != self.current_content and (
                ignored_content is None or current_content != ignored_content.content
            ):
                self.current_content = current_content
                self.last_update_time = time.time()
                self.queue.put(
                    NewKeyboardContent(
                        time=self.last_update_time, content=self.current_content
                    )
                )

            time.sleep(self.check_interval)
