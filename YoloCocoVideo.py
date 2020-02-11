# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:02:31 2020

@author: Alexandre Banon
"""

# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import sys



class YoloCocoVideo:
    
    def __init__(self,
                 arg_video      = "ressources\\TikTok.mp4",
                 arg_yolo       = "yolo-coco",
                 arg_confidence = 0.5,
                 arg_threshold  = 0.3,
                 arg_output     = "ressources"):
    
        self.video_path  = arg_video
        self.yolo        = arg_yolo
        self.confidence  = arg_confidence
        self.threshold   = arg_threshold
        self.output_path = arg_output
        
        self.output_file = os.path.join(self.output_path,
                                        "BOXED_" + os.path.splitext(os.path.basename(self.video_path))[0]) + ".avi"
        
        self.writer = None
        (self.W, self.H) = (None, None)
        self.ide = 0

        debut = time.time()
        (self.LABELS, self.COLORS, self.ln, self.net, self.vs, self.total) = self.loadingYoloCoco()
        self.elap = self.LaunchOnVideo(self.confidence, self.threshold)
        print("Fin : ", time.time()-debut)
        
        
    def loadingYoloCoco(self):
        # load the COCO class labels our YOLO model was trained on
        labelsPath = os.path.sep.join([self.yolo, "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")
        
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
        
        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([self.yolo, "yolov3.weights"])
        configPath = os.path.sep.join([self.yolo, "yolov3.cfg"])
        
        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
        # initialize the video stream, pointer to output video file, and
        # frame dimensions
        vs = cv2.VideoCapture(self.video_path)

        # try to determine the total number of frames in the video file
        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() else cv2.CAP_PROP_FRAME_COUNT
            total = int(vs.get(prop))
            print("[INFO] {} total frames in video".format(total))
        
        # an error occurred while trying to determine the total
        # number of frames in the video file
        except:
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1
            
        return (LABELS, COLORS, ln, net, vs, total)
    
    
    def LaunchOnVideo(self, arg_confidence, arg_threshold):  
        # read the next frame from the file
        (grabbed, frame) = self.vs.read()
            
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:        
            # release the file pointers
            print("\n[INFO] cleaning up...")
            self.writer.release()
            self.vs.release()
            
            self.writer = None
            (self.W, self.H) = (None, None)
            self.ide = 0
            self.elap = None
            
            return (not grabbed)
            
        # if the frame dimensions are empty, grab them
        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]
    
        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        
        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []
    
        # loop over each of the layer outputs
        for output in layerOutputs:
            
            # loop over each of the detections
            for detection in output:
                
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > arg_confidence:
                    
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([self.W, self.H, self.W, self.H])
                    (centerX, centerY, width, height) = box.astype("int")
                    
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
                    
        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, arg_confidence, arg_threshold)
        
        # ensure at least one detection exists
        if len(idxs) > 0:
            
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
        # check if the video writer is None
        if self.writer is None:
            
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            
            self.writer = cv2.VideoWriter(self.output_file,
                                          fourcc,
                                          30,
                                          (frame.shape[1], frame.shape[0]),
                                          True)
            
            # some information on processing single frame
            if self.total > 0:
                elap = (end - start)
                print("[INFO] single frame took {:.4f} seconds".format(elap))
                print("[INFO] estimated total time to finish: {:.4f}".format(elap * self.total))
                
            # write the output frame to disk
            self.writer.write(frame)
            self.ide += 1
            
            return elap
    
        # write the output frame to disk
        self.writer.write(frame)
        
        ph = "\rDetection over the video : {0} %        ".format(round(100.*self.ide/(self.total-1),2))
        sys.stdout.write(ph)
        sys.stdout.flush()
        self.ide += 1
        return False


if __name__ == '__main__':
    
    img_name = "TikTok"
    #img_name = "MOV_2707"

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--video",                  default="videos\\" + img_name + ".mp4", help="path to input video")
    ap.add_argument("-y", "--yolo",                   default="yolo-coco", help="base path to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold",  type=float, default=0.3, help="threshold when applyong non-maxima suppression")
    ap.add_argument("-o", "--output",                 default="output", help="path to output image")
    args = vars(ap.parse_args())

    yolo = YoloCocoVideo(args["video"],
                         args["yolo"],
                         args["confidence"],
                         args["threshold"],
                         args["output"])
    
    duration = (yolo.elap*yolo.total)
    input("Temps estimé :        {0} mn {1} s".format(int(duration/60.),round(duration%60)))
    
    grabbed = False
    # loop over frames from the video file stream
    while not grabbed:
        grabbed = yolo.LaunchOnVideo(args["confidence"],
                                     args["threshold"])