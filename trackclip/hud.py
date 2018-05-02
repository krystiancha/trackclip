from cv2.cv2 import rectangle, putText, FONT_HERSHEY_DUPLEX, LINE_AA
from numpy import copy

from trackclip.player_state import PlayerState
from trackclip.tracking_object import TrackingObject
from trackclip.utilities import rect_vertices


class HUDColors:
    base03 = (54, 43, 0)
    base02 = (66, 54, 7)
    base01 = (117, 110, 88)
    base00 = (131, 123, 101)
    base0 = (150, 148, 131)
    base1 = (161, 161, 147)
    base2 = (213, 232, 238)
    base3 = (227, 246, 253)
    yellow = (0, 137, 181)
    orange = (22, 75, 203)
    red = (47, 50, 220)
    magenta = (130, 54, 211)
    violet = (196, 113, 108)
    blue = (201, 139, 38)
    cyan = (152, 161, 42)
    green = (0, 153, 133)


class HUD:
    player_state: PlayerState

    def __init__(self, player_state: PlayerState) -> None:
        self.player_state = player_state
        self.frame_count = 1
        self.fps = self.player_state.fps
        self.colors = HUDColors

    def render(self, org_frame):
        frame = copy(org_frame)

        if self.frame_count % (int(round(self.player_state.fps / 2)) or 1) == 0:
            self.fps = self.player_state.fps
        self._put_text(
            frame,
            "Previev FPS: {0:05.01f}     Actual FPS: {1:05.01f}".format(self.fps, self.player_state.original_fps),
            (10, 20),
            self.colors.cyan,
        )

        if self.player_state.selection:
            p1, p2, p3, p4 = rect_vertices(self.player_state.selection, integers=True)
            rectangle(frame, p1, p3, self.colors.green, 2, 1)

        tracking_object: TrackingObject
        for idx, tracking_object in enumerate(self.player_state.tracking_objects):
            if tracking_object.rect:
                p1, p2, p3, p4 = rect_vertices(tracking_object.rect, integers=True)
                rectangle(frame, p1, p3, self.colors.blue, 2, 1)
                self._put_text(frame, tracking_object.label + ("|" if tracking_object.label_typing_in_progress else ""), p4, self.colors.blue, 1)
                self._put_text(frame, "Obj {} {}: TRACKING".format(idx + 1, tracking_object.label),
                               (int(round(5*frame.shape[1]/6)), 20 + 25 * idx), self.colors.green)
            else:
                self._put_text(frame, "Obj {} {}: LOST".format(idx + 1, tracking_object.label),
                               (int(round(5*frame.shape[1]/6)), 20 + 25 * idx), self.colors.yellow)

        self.frame_count += 1

        return frame

    def render_output(self, frame):
        tracking_object: TrackingObject
        for idx, tracking_object in enumerate(self.player_state.tracking_objects):
            if tracking_object.rect:
                p1, p2, p3, p4 = rect_vertices(tracking_object.rect, integers=True)
                rectangle(frame, p1, p3, self.colors.blue, 2, 1)
                self._put_text(frame, tracking_object.label, p4, self.colors.green)

    @staticmethod
    def _put_text(img, text, org, color, font_scale=0.5, font_face=FONT_HERSHEY_DUPLEX, thickness=1, line_type=LINE_AA,
                  bottom_left_origin=False):
        return putText(img, text, org, font_face, font_scale, color, thickness, line_type, bottom_left_origin)