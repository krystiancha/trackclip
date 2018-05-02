from cv2.cv2 import VideoCapture, imshow, waitKey, rectangle, Tracker, TrackerKCF_create, TickMeter, putText, \
    FONT_HERSHEY_SIMPLEX, VideoWriter, VideoWriter_fourcc, CAP_PROP_FPS
from numpy import copy

from trackclip.selector import Selector


class Player:
    writer: VideoWriter
    tracker: Tracker

    def __init__(self, input_filename: str, output_filename: str, codec: str, window_name: str) -> None:

        # OPTIONS
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.window_name = window_name

        self.writer = None
        if self.output_filename:
            codec = VideoWriter_fourcc(*(codec or 'XVID'))
            self.writer = VideoWriter(output_filename, codec, 30, (1280, 720))

        self.capture = VideoCapture(input_filename)
        if not self.capture.isOpened():
            raise Exception("The capture could not be opened")

        ok, self.org_frame = self.capture.read()
        if not ok:
            raise Exception("The capture could not be read")

        self.fps = self.capture.get(CAP_PROP_FPS) or 60

        imshow(self.window_name, self.org_frame)

        self.play = False
        self.tracker = None
        self.rect = None
        self.label = ""

        self.dynamic_rect = Selector(self.window_name)
        self.dynamic_rect.on_selecting = self.on_selecting
        self.dynamic_rect.on_selected = self.on_selected

        self.meter = TickMeter()

    def update(self):
        self.meter.start()
        if self.play:
            ok, self.org_frame = self.capture.read()
            if not ok:
                raise Exception("The capture could not be read")
            if self.tracker:
                ok, self.rect = self.tracker.update(self.org_frame)
                if not ok:
                    self.rect = None

        frame = copy(self.org_frame)

        if self.rect:
            x, y, w, h = self.rect
            p1 = (int(x), int(y))
            p2 = (int(x + w), int(y + h))
            rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            putText(frame, self.label, (p2[0] + 5, p1[1] + 5), FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        elif not self.tracker and self.dynamic_rect.points[0] != self.dynamic_rect.points[1]:
            rectangle(frame, self.dynamic_rect.points[0], self.dynamic_rect.points[1], (0, 255, 0), 2, 1)

        imshow(self.window_name, frame)

        if self.play and self.writer:
            frame2 = copy(self.org_frame)
            if self.rect:
                x, y, w, h = self.rect
                p1 = (int(x), int(y))
                p2 = (int(x + w), int(y + h))
                rectangle(frame2, p1, p2, (255, 0, 0), 2, 1)
                putText(frame2, self.label, (p2[0] + 5, p1[1] + 5), FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            self.writer.write(frame2)

        self.meter.stop()
        wait_ms = max(1, 1000.0 / self.fps - self.meter.getTimeMilli())
        self.meter.reset()

        key = waitKey(int(wait_ms)) & 0xff
        if key == 27:
            self.capture.release()
            if self.writer:
                self.writer.release()
            return -1
        elif key == 32:
            self.play = not self.play
        elif key == 83:
            self.fps = self.fps * 2
        elif key == 81:
            self.fps = self.fps / 2

    def on_selecting(self, rect):
        self.tracker = None
        self.rect = None

    def on_selected(self, rect):
        self.tracker = TrackerKCF_create()
        self.tracker.init(self.org_frame, rect)
        self.rect = rect
