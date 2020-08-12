#!/usr/bin/env bash
echo "Download Yolov3 weights"

gdown https://drive.google.com/uc?id=11a460kYkHaQorJm8FnZPoRRj4vqGEWGC -O yolov3.weights

gdown https://drive.google.com/uc?id=1bE862pLJtWeyasmp9Ak8E02ly1EJJzin -O yolov3_7000.weights

mv yolov3.weights source_pretrained_yolo/yolov3/yolo-coco
mv yolov3_7000.weights source_custom_yolo/yolov3/yolo-mask


