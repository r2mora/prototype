import time
import picamera
import threading

count = 0

def start_timer():
    global count
    count += 1
    image = "snap{0}.jpg".format(count)
    camera = picamera.PiCamera()
    camera.resolution = (800,600)
    camera.capture("static/"+image)
    camera.close()
    print("save completed, count : {}".format(count))

    timer = threading.Timer(5,start_timer)
    timer.start()
    if count >= 5:
        timer.cancel()
        print("timer exit")

if __name__ == "__main__":
    start_timer()
