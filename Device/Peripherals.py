
import cv2, pyaudio, keyboard
from .Components import ElectronicComponents
class Micro(ElectronicComponents):
    def __init__(self, record_seconds_default=5, rate=44100, chuck=1024, channels=1, format=pyaudio.paInt16, name=None):
        super().__init__(name=name, board=None, pin=0)
        self.record_seconds_default = record_seconds_default
        self.rate = rate
        self.chuck = chuck
        self.channels = channels
        self.format = format
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, 
                                      channels=self.channels, 
                                      rate=self.rate, 
                                      input=True,
                                      frames_per_buffer=self.chuck)
        
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
    
    def getFrame(self, record_seconds=None):
        frames = []
        time = 0
        if not record_seconds is None: time = record_seconds
        else: time = self.record_seconds_default
        
        for _ in range(0, int(self.rate / self.chuck * time)):
                data = self.stream.read(self.chuck)
                frames.append(data)
            
        return frames
    
    def playFrame(self, frames):
        for frame in frames:
            self.stream.write(frame)

class Camera(ElectronicComponents):
    def __init__(self, COM, resolution=[1280, 720], flip=False, name=None):
        super().__init__(name=name, board=None, pin=0)
        self.COM = COM
        self.resolution = resolution
        self.flip = flip

        self.cap = cv2.VideoCapture(self.COM)
        if not self.cap.isOpened():
            raise RuntimeError("Camera error")
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
    def getFrame(self):
        ret, image = self.cap.read()
        if not ret: image = None
        elif self.flip: image = cv2.flip(image, 1)
        return image
    
    def liveView(self, frame):
        cv2.imshow("Camera", frame)
         