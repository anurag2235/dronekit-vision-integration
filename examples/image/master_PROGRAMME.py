# !/usr/bin/env python
import multiprocessing
import cv2
import os
import sys,getopt
import signal
import time
from edge_impulse_linux.image import ImageImpulseRunner
lista=[]
listb=[]
listc=[]
def vision():
    runner = None
    show_camera = True
    if (sys.platform == 'linux' and not os.environ.get('DISPLAY')):
        show_camera = False
    def now():
        return round(time.time() * 1000)
    def sigint_handler(sig, frame):
        print('Interrupted')
        if (runner):
            runner.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    model = "un64.eim"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)
    with ImageImpulseRunner(modelfile) as runner:
            try:
                model_info = runner.init()
                labels = model_info['model_parameters']['labels']
                videoCaptureDeviceId = int(0)  # if not automatically detect add id here inside bracket...,
                camera = cv2.VideoCapture(videoCaptureDeviceId)
                ret = camera.read()[0]
                if ret:
                    backendName = camera.getBackendName()
                    w = camera.get(3)
                    h = camera.get(4)
                    print("Camera %s (%s x %s) in port %s selected." % (backendName, h, w, videoCaptureDeviceId))
                    camera.release()
                else:
                    raise Exception("Couldn't initialize selected camera.")
                next_frame = 0  # limit to ~10 fps here
                for res, img in runner.classifier(videoCaptureDeviceId):
                    if (next_frame > now()):
                        time.sleep((next_frame - now()) / 1000)
                    if "classification" in res["result"].keys():
                        print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                        for label in labels:
                            score = res['result']['classification'][label]
                            print('%s: %.2f\t' % (label, score), end='')
                        print('', flush=True)
                    elif "bounding_boxes" in res["result"].keys():
                        for bb in res["result"]["bounding_boxes"]:
                            c=len(res["result"]["bounding_boxes"])
                            if c==1:
                             lista.append(bb['x'])
                             listb.append(bb['y'])
                             listc.append(1)
                            else:
                             lista.append(0)
                             listb.append(0)
                             listc.append(0)
                            img = cv2.rectangle(img, (bb['x'], bb['y']),
                                                (bb['x'] + bb['width'], bb['y'] + bb['height']), (255, 0, 0), 1)
                    if (show_camera):
                        cv2.imshow('edgeimpulse', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                        if cv2.waitKey(1) == ord('q'):
                            break
                    next_frame = now() + 1  # you can control speed here....
            finally:
                if (runner):
                    runner.stop()
def dronekit():
    print(lista[-1],listb[-1],listc[-1])
if __name__ == "__main__":
# creating multiple processes
 proc1 = multiprocessing.Process(target=vision())
 proc2 = multiprocessing.Process(target=dronekit())
# Initiating process 1
 proc1.start()
# Initiating process 2
 proc2.start()
