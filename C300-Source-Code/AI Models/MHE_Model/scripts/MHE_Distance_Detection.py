from ultralytics import YOLO
import depthai as dai
import cv2
import supervision as sv
import numpy as np
from scipy.spatial import distance as dist
import math
import time
import countItem
import reportFile

# Load YOLO model
model = YOLO("..\\MHE_Model\\train\\weights\\best.pt") #MHE Model

def midpoint(ptA, ptB):
    # Calculate the midpoint between two points
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def box_to_points(box):
    # Convert box coordinates to top-left and bottom-right points
    x_min, y_min, x_max, y_max = box
    ptA = (x_min, y_min)  # Top-left corner
    ptB = (x_max, y_max)  # Bottom-right corner
    return ptA, ptB

def avgCoordinateAxis(box): 
    x_min, y_min, x_max, y_max = box
    x_avg = x_min + x_max * 0.5
    y_avg = y_min + y_max * 0.5

    return x_avg, y_avg

#Focal Length: 568.4
def calculate_distance(arr, frame):
    x_diff = abs((arr[1][0] - arr[0][0])**2)
    y_diff = abs((arr[1][1] - arr[0][1])**2)
    
    z_cm = abs((arr[1][2] - arr[0][2])**2)

    #print(arr[0][3])
    #print(arr[1][3])
    return math.sqrt(x_diff + y_diff + z_cm) / 1000 # Convert to M

def calHumanDist_From_MHE(arr, frame, index):
    # x_diff = abs((arr[1][0] - arr[0][0])**2)
    # y_diff = abs((arr[1][1] - arr[0][1])**2)
    
    # z_cm = abs((arr[1][2] - arr[0][2])**2)
    # return math.sqrt(x_diff + y_diff + z_cm) / 1000 # Convert to M
    indexOfMHE = 0
    for x in range(len(arr)):
        if x != index: 
            indexOfMHE = x

    x_diff = abs((arr[indexOfMHE][0] - arr[index][0])**2)
    y_diff = abs((arr[indexOfMHE][1] - arr[index][1])**2)
    
    z_cm = abs((arr[indexOfMHE][2] - arr[index][2])**2)
    return math.sqrt(x_diff + y_diff + z_cm) / 1000 # Convert to M




def setupCamera():
    # Create depthai pipeline
    pipeline = dai.Pipeline()

    # Create color camera node
    camRgb = pipeline.createColorCamera()
    xoutRgb = pipeline.createXLinkOut()
    xoutRgb.setStreamName("rgb")

    # Set color camera properties
    camRgb.setPreviewSize(1080, 720)
    camRgb.setInterleaved(False)
    camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

    #Create nodes

    # Create mono cameras
    monoLeft = pipeline.createMonoCamera()
    monoRight = pipeline.createMonoCamera()

    # Create stereo depth node
    stereo = pipeline.createStereoDepth()

    # Create XLinkOut for depth stream
    xoutDepth = pipeline.createXLinkOut()
    xoutDepth.setStreamName("depth")


    # Set mono camera properties
    #setResolution() sets the resolution of the mono cameras. (720p).
    #setBoardSocket() sets the board socket for the mono cameras. LEFT is assigned to monoLeft and RIGHT is assigned to monoRight. 
    monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
    monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    
    # Set stereo depth properties
    stereo.initialConfig.setConfidenceThreshold(245) #245 as stated in their document
    stereo.setRectifyEdgeFillColor(0)  # Black, to better see the cutout
    stereo.setLeftRightCheck(True)  # Enable left-right check for improved depth accuracy
    stereo.setExtendedDisparity(True) # Enable extended disparity range for accurate depth estimation of distant objects
    stereo.setSubpixel(False) # Disable subpixel disparity refinement for depth estimation at the pixel level
    stereo.setDepthAlign(dai.CameraBoardSocket.RGB) # Align depth map with RGB color image for accurate depth visualization and processing

    # Connect nodes in the pipeline
    monoLeft.out.link(stereo.left) # Connect the left mono camera output to the left input of the stereo depth node
    monoRight.out.link(stereo.right) # Connect the right mono camera output to the right input of the stereo depth node
    stereo.depth.link(xoutDepth.input)  # Connect the depth output of the stereo depth node to the input of the depth output queue

    # Connect color camera to output
    camRgb.preview.link(xoutRgb.input) # Connect the preview output of the color camera to the input of the RGB output queue

    return pipeline

def main():
    flag = False
    start_time = None
    detected_time = 0
    timeout_duration = 60  # seconds timeout

    
    # Create box annotator
    box_annotate = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    # Connect to device and start pipeline
    with dai.Device(setupCamera()) as device:
        # Get output queues
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)  # Retrieve the output queue for RGB frames
        qDepth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)  # Retrieve the output queue for depth frames


        while True:
            # Get color frame and depth frame
            inRgb = qRgb.get()  # Get the next RGB frame from the output queue
            inDepth = qDepth.get()  # Get the next depth frame from the output queue
            frame = inRgb.getCvFrame()  # Convert the RGB frame to a numpy array (OpenCV format)
            depthFrame = inDepth.getFrame()  # Get the depth frame as a numpy array
            depthFrame = cv2.resize(depthFrame, (frame.shape[1], frame.shape[0]))  # Resize the depth frame to match the dimensions of the RGB frame

            result = model(frame)[0]  # Perform object detection on the RGB frame using the YOLO model
            detections = sv.Detections.from_yolov8(result)  # Convert the detection results to a Detections object

            bb = []
            plotArr = []
            labels = [] # Initialize labels array for displaying
            
            for detection in detections:
                _, confidence, class_id, _ = detection # Unpack elements from the detection tuple
                if confidence > 0.2:
                    ptA, ptB = box_to_points(detection[0]) # Retrieve the two points from the detected object

                    midX, midY = midpoint(ptA, ptB) # Calculate the mid axis of the object


                    depth = depthFrame[int(midY), int(midX)] / 1000  # Calculate the distance between the camera and the object using depthFrame
                    x_avg, y_avg = avgCoordinateAxis(detection[0])
                    class_name = model.model.names[class_id]
                    bb.append([x_avg,y_avg, depth, class_name])
                    plotArr.append([ptA,ptB])

                    # Add depth text to annotation
                    label = f"{model.model.names[class_id]} {confidence:0.2f}"  # Adding the text for the labels 
                    if depth is not None:
                        label += f" {depth:.2f}m"  # Adds the depth if it is not empty/zero

                    labels.append(label)  # Append it to the initialized array
            
               
            if len(bb) >= 2:
                # distance = round(calculate_distance(bb,frame),3)
                # plotLine(frame, plotArr, distance)
                humanDetected = False
                indexOfHuman = 0
                for x in range(len(bb)):
                    if (bb[x][3] == "human"):
                        print("Human Detected")
                        humanDetected = True
                        indexOfHuman = x
                    else:
                        print("No Humans in sight")
                        humanDetected = False

                if (humanDetected): 
                    distance = round(calHumanDist_From_MHE(bb,frame,indexOfHuman),3)
                    plotLine(frame, plotArr, distance)
                    if (distance < 3):
                        if not flag:
                            print("In not flag")
                            flag = True
                            start_time = time.time()

                        detected_time = time.time() - start_time
                        print("Detected Time: ", start_time)
                        if detected_time > timeout_duration:
                            print("Distance has been breach")
                            index = countItem.count_items_in_folder("Breach_Images\\MHE")
                            imgName = "MHE" + str(index+1) + ".jpg"
                            cv2.imwrite("Breach_Images/MHE/"+ imgName, box_annotate.annotate(scene=frame, detections=detections, labels=labels))
                            print("Image Saved.")
                            pathName = "Breach_Images/MHE/"+ imgName #Find Path of the image saved
                            urlName = reportFile.uploadImage(pathName) #Upload Image
                            print("Image Uploaded.")
                            reportFile.createReport("MHE", "MHE has been breach with a distance of " + str(round(distance,3)) + "meters", urlName)
                            #Reset the flag and start_time
                            flag = False
                            start_time = None
                            print("Report Created.")
                    else:
                        flag = False
                        start_time = None


            frame = box_annotate.annotate(scene=frame, detections=detections, labels=labels)

            
            cv2.imshow("YoloV8", frame)
            
            if cv2.waitKey(1) == ord('q'):
                break



def plotLine(frame, arr, distCM):
    pt1 = midpoint(arr[0][0], arr[0][1])  # Midpoint of the first object
    pt2 = midpoint(arr[1][0], arr[1][1])  # Midpoint of the second object
    pt1 = (int(pt1[0]), int(pt1[1]))  
    pt2 = (int(pt2[0]), int(pt2[1]))  
    frame = cv2.line(frame, pt1, pt2, (0, 0, 255), 2)  

    # Calculate the midpoint of the line
    mid_point = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)

   
    text = str(distCM) + "M apart"  
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    text_org = (mid_point[0] - text_size[0] // 2, mid_point[1] + text_size[1] // 2 - 10) 
    frame = cv2.putText(frame, text, text_org, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) , 2, cv2.LINE_AA)

    return frame

if __name__ == "__main__":
    main()