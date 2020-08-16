# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os

confidence_threshold = 0.5
nms_threshold = 0.3

# use pretrained YOLO on mask dataset
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/yolo-mask/"

# load the COCO class YOLO model was trained on
labelsPath = os.path.join(APP_ROOT, "yolo.names")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.join(APP_ROOT, "yolov3_7000.weights")

configPath = os.path.join(APP_ROOT, "yolov3.cfg")


# LOAD YOLO MODEL ONCE
def load_model():
	print("[DEBUG] loading YOLO from disk...")
	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	classes = open(labelsPath).read().strip().split("\n")
	
	# determine only the *output* layer names that we need from YOLO
	layers_names = net.getLayerNames()
	output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	# initialize a list of colors to represent each possible class label
	np.random.seed(42)
	colors = np.random.randint(0, 255, size=(len(classes), 3),
	dtype="uint8")

	return net, classes, colors, output_layers


def detect_object(image, net, classes, colors, output_layers, H, W, blob_size=(416, 416)):

	# Contructing a blob from the input image
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, blob_size,
					swapRB=True, crop=False)

	# Perform a forward pass of the YOLO object detector	
	net.setInput(blob)

	# Getting the outputs from the output layers
	start = time.time()
	layerOutputs = net.forward(output_layers)
	end = time.time()
	

	# show timing information on YOLO
	print("[DEBUG] YOLO took {:.6f} seconds".format(end - start))

	# Generate the boxes, confidences, and classIDs
	boxes, confidences, classIDs = generate_boxes_confidences_classids(layerOutputs, H, W, confidence_threshold)

	# Apply Non-Maxima Suppression to suppress overlapping bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

	if boxes is None or confidences is None or idxs is None or classIDs is None:
		raise '[ERROR] Required variables are set to None before drawing boxes on images.'

	# Draw labels and boxes on the image
	img = draw_labels_and_boxes(image, boxes, confidences, classIDs, idxs, colors, classes)

	return img


def generate_boxes_confidences_classids(layerOutputs, H, W, confidence_threshold):
	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability) of
			# the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
			if confidence > confidence_threshold:
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

	return boxes, confidences, classIDs

def draw_labels_and_boxes(image, boxes, confidences, classIDs, idxs, colors, classes):
	# If there are any detections
	if len(idxs) > 0:
		for i in idxs.flatten():
			# Get the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# Get the unique color for this class
			color = [int(c) for c in colors[classIDs[i]]]

			# Draw the bounding box rectangle and label on the image
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
			cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, color, 2)

			if (classes[classIDs[i]] == "face"):
				cv2.putText(image, "WEAR THE MASK", (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX,
				1.0, (0,0,255), 3)

	return image


def infer_image(img_path, output_dir, net, classes, colors, output_layers):
	image = cv2.imread(img_path)
	(H, W) = image.shape[:2]

	image = detect_object(image, net, classes, colors, output_layers, H, W)
	cv2.imwrite(output_dir, image)


def infer_realtime_webcam(net, classes, colors, output_layers):
	# count = 0
	video = cv2.VideoCapture(0)

	while(True):
		ret, frame = video.read()
		(H, W) = frame.shape[:2]

		frame = detect_object(frame, net, classes, colors, output_layers, H, W, blob_size=(320, 320))

		ret, jpeg = cv2.imencode('.jpg', frame)
		out = jpeg.tobytes()
		
		yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + out + b'\r\n\r\n')


def infer_video(vid_path, output_dir, net, classes, colors, output_layers):
	video = cv2.VideoCapture(vid_path)
	(H, W) = (None, None)
	out = None


	while(True):
		ret, frame = video.read()

		# Check if the complete video is read
		if not ret:
			break
			
		if W is None or H is None:
			(H, W) = frame.shape[:2]

		frame = detect_object(frame, net, classes, colors, output_layers, H, W)

		# Define the codec and create VideoWriter object
		if out is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			out = cv2.VideoWriter(output_dir,fourcc, 30, (frame.shape[1], frame.shape[0]), True)

		out.write(frame)
	

	print("[DEBUG INFER VIDEO] Done")
	out.release()
	video.release()