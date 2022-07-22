import cv2

with open("/home/kiran/Videos/longestkillshoot.mp4", "rb") as file:
    data = file.read()
# video = cv2.VideoCapture("/home/kiran/Videos/longestkillshoot.mp4")
# video = data from data variable
with open("./temp.mp4", "wb") as file:
    file.write(data)
video = cv2.VideoCapture("./temp.mp4")
duration = video.get(cv2.CAP_PROP_POS_MSEC)
frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
# count FPS
fps = video.get(cv2.CAP_PROP_FPS)
print(frame_count / fps, frame_count)
