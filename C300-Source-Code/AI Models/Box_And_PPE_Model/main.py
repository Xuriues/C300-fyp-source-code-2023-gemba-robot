from ultralytics import YOLO
import cv2
import supervision as sv
import argparse
import time
import countItem
import reportFile

#Comment/Uncomment the model you are using/not using.
model = YOLO("box_model\\train\\weights\\best.pt")
#model = YOLO("ppe_model\\train\\weights\\best.pt")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 Live Webcam")
    parser.add_argument(
        "--webcam-resolution",
        default=[408, 720],
        nargs=2,
        type=int
    )

    return parser.parse_args()


def main():
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
        labels = []  # Initialize labels array for displaying

        for detection in detections:
            _, confidence, class_id, _ = detection

            if confidence > 0.5:
                label = f"{model.model.names[class_id]} {confidence:.2f}"
                labels.append(label)
                current_class = model.model.names[class_id]

                if current_class == "false":
                    if not flag:
                        print("This is false")
                        flag = True
                        start_time = time.time()  # Starts timer

                    detected_time = time.time() - start_time

                    if detected_time > timeout_duration:
                        # Perform the action after 5 seconds
                        print("Detected false for more than 5 seconds proceeding to save image")
                        index = countItem.count_items_in_folder(
                            "Breach_Images\\Boxes")  # Setting index for the image name
                        imgName = "Boxes" + str(
                            index + 1) + ".jpg"  # Set Image name if this is for boxes change PPE to Boxes
                        cv2.imwrite("Breach_Images/Boxes/" + imgName,
                                    box_annotate.annotate(scene=frame, detections=detections, labels=labels))
                        print("Image Saved.")
                        pathName = "Breach_Images/Boxes/" + imgName  # Find Path of the image saved
                        urlName = reportFile.uploadImage(pathName)  # Upload Image
                        print("Image Uploaded.")
                        # createReport("Boxes|PPE|MHE", Description, urlName) 4 you it'll be only PPE or Boxes
                        reportFile.createReport("Boxes", "Boxes has been breach", urlName)
                        # Reset the flag and start_time
                        flag = False
                        start_time = None
                        print("Report Created.")
                        break
                else:
                    flag = False
                    start_time = None

            frame = box_annotate.annotate(scene=frame, detections=detections, labels=labels)

            cv2.imshow("YoloV8", frame)

            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    main()