# Mask detection Yolov3 Web Demo (Image + Webcam) - MaskUp 

The repo contains two demonstrations:
- Pretrained Yolov3 on COCO dataset
- Custom Yolov3 on Face Mask dataset

### Installation

Clone repository
```
git clone <repo url>
```

Create and activate virtual environment for python development
```
virtualenv env
source env/bin/activate
```

Install libraries
```
pip install -r requirements.txt
```
Give permission to .sh file
```
chmod +x download.sh
```

Activate .sh file to download yolov3 models
```
./download.sh
```
Then **respectively** ```cd``` into each folder and call ```flask run```, the website is deployed to localhost: ```http://127.0.0.1:5000/```

### Technology:
- Frontend: HTML + CSS + Javascript
- Backend: Flask
- CV Libraries: OpenCV

### References: 
- [Pyimagesearch Yolo Object Detection](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)
- [Yolov3 webcam](https://github.com/iArunava/YOLOv3-Object-Detection-with-OpenCV)
- [Novel Covid API](https://github.com/disease-sh/api)
- [UI for homepage](https://www.youtube.com/watch?v=zBPHBnSIzfk)
- [gdown](https://pypi.org/project/gdown/)
- [Face mask dataset](https://www.miai.vn/thu-vien-mi-ai/)
