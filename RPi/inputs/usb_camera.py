import cv2

cap = cv2.VideoCapture(0) # Standard index

def get_usb_frame():
    ret, frame = cap.read()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)