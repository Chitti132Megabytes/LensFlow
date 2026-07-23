from PySide6.QtCore import QThread, Signal
from backend.camera_engine import CameraEngine


class CameraThread(QThread):

    frame_ready = Signal(object)

    def __init__(self):
        super().__init__()

        self.running = False
        self.engine = CameraEngine()

    def run(self):

        self.running = True

        try:
            self.engine.start()

        except RuntimeError as e:
            print(e)
            return

        while self.running:

            frame = self.engine.read()

            if frame is None:
                continue

            self.frame_ready.emit(frame)

        self.engine.stop()

    def stop(self):

        self.running = False
        self.wait()