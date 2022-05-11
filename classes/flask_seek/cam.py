import cv2
import rend

from seekcamera import (
    SeekCameraIOType,
    SeekCameraColorPalette,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCamera,
    SeekFrame,
)

class seek_camera():
    def __init__(self):
        pass
    
    def on_frame(self, _camera, camera_frame, renderer):
        with renderer.frame_condition:
            renderer.frame = camera_frame.color_argb8888
            renderer.frame_condition.notify()


    def on_event(self, camera, event_type, event_status, renderer):
        print("{}: {}".format(str(event_type), camera.chipid))

        if event_type == SeekCameraManagerEvent.CONNECT:
            if renderer.busy:
                return

            renderer.busy = True
            renderer.camera = camera

            renderer.first_frame = True

            camera.color_palette = SeekCameraColorPalette.TYRIAN

            camera.register_frame_available_callback(self.on_frame, renderer)
            camera.capture_session_start(SeekCameraFrameFormat.COLOR_ARGB8888)

        elif event_type == SeekCameraManagerEvent.DISCONNECT:
            if renderer.camera == camera:
                camera.capture_session_stop()
                renderer.camera = None
                renderer.frame = None
                renderer.busy = False

        elif event_type == SeekCameraManagerEvent.ERROR:
            print("{}: {}".format(str(event_status), camera.chipid))

        elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
            return


    def get_frame(self):
        with SeekCameraManager(SeekCameraIOType.USB) as manager:
            renderer = rend.Renderer()
            manager.register_event_callback(self.on_event, renderer)

            while True:
                with renderer.frame_condition:
                    if renderer.frame_condition.wait(150.0 / 1000.0):
                        img = renderer.frame.data
                        #cv2.imshow(window_name, img)
                        imgencode = cv2.imencode('.jpg', img)[1]
                        string_data = imgencode.tostring()
                        yield(b'--frame\r\n'
                  b'Content-Type: text/plain\r\n\r\n' + string_data
                  + b'\r\n\r\n')
                        
            del(renderer)
    