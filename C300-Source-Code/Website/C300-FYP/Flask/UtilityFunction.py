#Other functions needed for MHE & Chatbot to work.
from ultralytics import YOLO
import cv2
import supervision as sv
import argparse
import time
import pyttsx3

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
    x_avg = x_min + x_max / 2
    y_avg = y_min + y_max / 2

    return x_avg, y_avg

#Focal Length: 568.4
def calculate_distance(arr, frame):
    x_diff = abs((arr[1][0] - arr[0][0])**2)
    y_diff = abs((arr[1][1] - arr[0][1])**2)
    z_axis = abs((arr[1][2] - arr[0][2])**2)

    return math.sqrt(x_diff + y_diff + z_axis) / 1000 # Convert to M

def plotLine(frame, arr):
    pt1 = midpoint(arr[0][0], arr[0][1])  # Midpoint of the first object
    pt2 = midpoint(arr[1][0], arr[1][1])  # Midpoint of the second object
    pt1 = (int(pt1[0]), int(pt1[1]))  # Convert to integers
    pt2 = (int(pt2[0]), int(pt2[1]))  # Convert to integers
    frame = cv2.line(frame, pt1, pt2, (0, 0, 255), 2)  # Plot a red line between the two objects

    # Calculate the midpoint of the line
    return frame

def generateSpeech(text):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id) #sets voice
    engine.setProperty('rate', 125) #changes the speed of the voice
    engine.setProperty('volume',1.0) #setting up volume level between 0 and 1
    engine.say(text)
    engine.runAndWait()