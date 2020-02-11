# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 20:05:33 2020

@author: Alexandre Banon
"""

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os



class YoloCocoImage:
    
    def __init__(self,
                 arg_image      = "ressources\\DSC_0506.JPG",
                 arg_yolo       = "yolo-coco",
                 arg_confidence = 0.5,
                 arg_threshold  = 0.3,
                 arg_output     = "ressources"):

        self.image_path  = arg_image
        self.yolo        = arg_yolo
        self.confidence  = arg_confidence
        self.threshold   = arg_threshold
        self.output_path = arg_output
        
        self.output_file = os.path.join(self.output_path, "BOXED_" + os.path.basename(self.image_path))

        debut = time.time()
        (self.LABELS, self.COLORS, self.layerOutputs, self.image) = self.loadingYoloCoco()
        self.LaunchOnImage(self.confidence, self.threshold)
        print("Fin : ", time.time()-debut)


    def loadingYoloCoco(self):
        # load the COCO class labels our YOLO model was trained on
        labelsPath = os.path.sep.join([self.yolo, "coco.names"])
        LABELS     = open(labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
        
        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([self.yolo, "yolov3.weights"])
        configPath  = os.path.sep.join([self.yolo, "yolov3.cfg"])
        
        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        
        # load our input image and grab its spatial dimensions
        image = cv2.imread(self.image_path)
  
        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        
        # show timing information on YOLO
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        
        return (LABELS, COLORS, layerOutputs, image)


    def LaunchOnImage(self, arg_confidence, arg_threshold):
        start = time.time()
        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes       = []
        confidences = []
        classIDs    = []
        
        # image sizes
        (H, W) = self.image.shape[:2]

        # loop over each of the layer outputs
        for output in self.layerOutputs:
            
        	# loop over each of the detections
        	for detection in output:
                
        		# extract the class ID and confidence (i.e., probability) of
        		# the current object detection
        		scores     = detection[5:]
        		classID    = np.argmax(scores)
        		confidence = scores[classID]
                
        		# filter out weak predictions by ensuring the detected
        		# probability is greater than the minimum probability
        		if confidence > arg_confidence:
        			
                    # scale the bounding box coordinates back relative to the
        			# size of the image, keeping in mind that YOLO actually
        			# returns the center (x, y)-coordinates of the bounding
        			# box followed by the boxes' width and height
        			box = detection[0:4] * np.array([W, H, W, H])
        			(centerX, centerY, width, height) = box.astype("int")
        			
                    # use the center (x, y)-coordinates to derive the top and
        			# and left corner of the bounding box
        			x = int(centerX - (width / 2))
        			y = int(centerY - (height / 2))
        			
                    # update our list of bounding box coordinates, confidences,
        			# and class IDs
        			boxes.append([x, y, int(width), int(height)])
        			confidences.append(float(confidence))
        			classIDs.append(classID)
                    
        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, arg_confidence, arg_threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            
        	# loop over the indexes we are keeping
        	for i in idxs.flatten():
                
        		# extract the bounding box coordinates
        		(x, y) = (boxes[i][0], boxes[i][1])
        		(w, h) = (boxes[i][2], boxes[i][3])
        		
                # draw a bounding box rectangle and label on the image
        		color = [int(c) for c in self.COLORS[classIDs[i]]]
        		cv2.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
        		text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
        		cv2.putText(self.image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        end = time.time()
        # show timing information on YOLO
        print("[INFO] Detection took {:.6f} seconds".format(end - start))
        
        # show the output image
        cv2.imwrite(self.output_file, self.image)
        
#        cv2.imshow("Image", self.image)
#        cv2.waitKey(0)
#        cv2.destroyWindow('Image')


if __name__ == '__main__':
    
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",                  default="images\\JPG_dl1577292314664.jpg", help="path to input image")
    ap.add_argument("-y", "--yolo",                   default="yolo-coco", help="base path to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold",  type=float, default=0.3, help="threshold when applying non-maxima suppression")
    ap.add_argument("-o", "--output",                 default="output", help="path to output image")
    args = vars(ap.parse_args())
    
    yolo = YoloCocoImage(args["image"],
                         args["yolo"],
                         args["confidence"],
                         args["threshold"],
                         args["output"])
