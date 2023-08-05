import pyrebase
from datetime import datetime
import cloudinary.uploader
import requests

def teleNotification(message):

    apiToken = '6381126305:AAGAZ9TZIGWqfuht3uoZquRJk_QJUU7cYaE'
    chatID = '-1001899457951'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def uploadImage(filePath):
    cloudinary.config( 
      cloud_name = "djqp3t4az", 
      api_key = "654152824691592", 
      api_secret = "i0Zuhzx0KlngGSv31yiwPdOl9dA" 
    )
    result = cloudinary.uploader.upload(filePath, use_filename=True, unique_filename=False)
    return result['secure_url']

# 2nd Node Consist of ONLY: PPE MHE Boxes

def setupFireBase(): 
    firebaseConfig = {
      "apiKey": "AIzaSyBp35in9gzSvIvJ74xdoy1pZiFplPj9bHc",
      "authDomain": "test-proj-ff62f.firebaseapp.com",
      "databaseURL": "https://test-proj-ff62f-default-rtdb.asia-southeast1.firebasedatabase.app/",
      "projectId": "test-proj-ff62f",
      "storageBucket": "test-proj-ff62f.appspot.com",
      "messagingSenderId": "959978182728",
      "appId": "1:959978182728:web:bfcea92855013b7d22607d"
    };

    return pyrebase.initialize_app(firebaseConfig)


conn = setupFireBase()
fireDatabase = conn.database()


def findIndex(topic): 
    starting_id = 1
    snapshot = fireDatabase.child("Reports").child(topic).get()

    if snapshot.each() is not None:
        starting_id += len(snapshot.each())

    return starting_id



def createReport(topic, description, urlName):
    report_date = datetime.now().strftime("%d/%m/%Y")
    report_time = datetime.now().strftime("%H:%M:%S")
    UID = topic+str(findIndex(topic))
    data = {
        "Id": UID,
        "Topic": topic,
        "date": report_date,
        "time": report_time,
        "Description": description,
        "Report_Status": True,
        "urlImg": urlName,
        "ReasonForClosure": "",
        "AdditionalInfo": ""
    }

    try:
        fireDatabase.child("Reports").child(topic).child(UID).set(data)
        teleNotification("Incident Report has been created please do check the website UID: " + UID + "\n\n" + urlName)
    except Exception as e:
        print("Error occurred while creating the report:", e)

