#Combination of Jordon, Shaun, Sanni task
import pyttsx3
import torch
import streamlit as st
import random
import time
import cv2
import supervision as sv
import argparse
import time

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from datasets import load_dataset
from ultralytics import YOLO

import UtilityFunction
import reportFile
import countItem

def parse_arguments () -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 Live Webcam")
    parser.add_argument(
        "--webcam-resolution",
        default=[408,720],
        nargs = 2,
        type = int
    )

    return parser.parse_args()

def Jordon_Model(model, modelName):
    args = parse_arguments()
    w, h = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    box_annotate = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    flag = False
    start_time = None
    detected_time = 0
    timeout_duration = 5  # 5 seconds timeout

    while True:
        ret, frame = cap.read()
        result = model(frame)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [] # Initialize labels array for displaying

        for detection in detections:
            _, confidence, class_id, _ = detection
                
            if confidence > 0.4:
                label = f"{model.model.names[class_id]} {confidence:.2f}"
                labels.append(label)
                current_class = model.model.names[class_id]

                if current_class == "false":
                    if not flag:
                        flag = True
                        start_time = time.time()  # Starts timer

                    detected_time = time.time() - start_time
                    if detected_time > timeout_duration:
                        index = countItem.count_items_in_folder(f"Breach_Images\{modelName}")
                        imgName = modelName + str(index + 1) + ".jpg"
                        cv2.imwrite(f"Breach_Images/{modelName}/" + imgName,box_annotate.annotate(scene=frame, detections=detections, labels=labels))
                        pathName = f"Breach_Images/{modelName}/" + imgName

                        urlName = reportFile.uploadImage(pathName)

                        reportFile.createReport(modelName, f"{modelName} has been breach", urlName)
                        # Reset the flag and start_time

                        flag = False
                        start_time = None

                else:
                    flag = False
                    start_time = None


            frame = box_annotate.annotate(scene=frame, detections=detections, labels=labels)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def Shaun_Model(model):
    args = parse_arguments()
    w, h = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    box_annotate = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    flag = False
    start_time = None
    detected_time = 0
    timeout_duration = 5  # 5 seconds timeout

    while True:
        ret, frame = cap.read()
        result = model(frame)[0]
        detections = sv.Detections.from_yolov8(result)
        bb = []
        plotArr = []
        labels = [] # Initialize labels array for displaying

        for detection in detections:
            _, confidence, class_id, _ = detection
                
            if confidence > 0.3:
                ptA, ptB = UtilityFunction.box_to_points(detection[0])

                midX, midY = UtilityFunction.midpoint(ptA, ptB)

                x_avg, y_avg = UtilityFunction.avgCoordinateAxis(detection[0])

                bb.append([x_avg,y_avg])
                plotArr.append([ptA,ptB])

                label = f"{model.model.names[class_id]} {confidence:.2f}"
                labels.append(label)

            if len(bb) >= 2:
            	UtilityFunction.plotLine(frame, plotArr)
            frame = box_annotate.annotate(scene=frame, detections=detections, labels=labels)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def chatbotAnswer(prompt):
    tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b")
    model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True)
    generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True)
    print("Question: " + prompt)
    res = generate_text(prompt)
    ans = res[0]["generated_text"]
    print("Answer is: " + ans)
    return ans


