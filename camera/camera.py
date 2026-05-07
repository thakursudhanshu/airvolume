import cv2
import threading
from queue import Queue

class WebcamCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame_queue = Queue(maxsize=1)
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.cap.release()

    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if not self.frame_queue.empty():
                    try:
                        self.frame_queue.get_nowait()
                    except:
                        pass
                self.frame_queue.put(frame)

    def get_frame(self):
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None