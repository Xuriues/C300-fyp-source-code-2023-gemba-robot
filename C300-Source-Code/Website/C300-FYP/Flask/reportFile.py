#This Task was done by Kezia Widjaja 
import pyrebase
from datetime import datetime
import cloudinary.uploader
import requests

#Function of telegram notification to be sent out when a report is created.
def teleNotification(message):

    apiToken = '6381126305:AAGAZ9TZIGWqfuht3uoZquRJk_QJUU7cYaE'
    chatID = '-1001899457951'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

#Uploads the image file to Cloudinary, use_filename is true because we want it to use our naming convention and not the random filename that cloudinary will use.
def uploadImage(filePath):
    cloudinary.config( 
      cloud_name = "djqp3t4az", 
      api_key = "654152824691592", 
      api_secret = "i0Zuhzx0KlngGSv31yiwPdOl9dA" 
    )
    result = cloudinary.uploader.upload(filePath, use_filename=True, unique_filename=False)
    return result['secure_url']

#Set up the connection string to firebase VIA pyrebase4
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

# Save the intilialization of the firebase to conn & retrieves the database from the dbURL and saves it in fireDatabase
conn = setupFireBase()
fireDatabase = conn.database()

#Topic consist of MHE, PPE, Boxes
#Returns the index of the specific child node, if can't find any returns 1 (which is the starting)
def findIndex(topic): 
    starting_id = 1
    snapshot = fireDatabase.child("Reports").child(topic).get()

    if snapshot.each() is not None:
        starting_id += len(snapshot.each())

    return starting_id



def createReport(topic, description, urlName):
    #Easier to retrieve date and time individually in the Report Page of the website
    report_date = datetime.now().strftime("%d/%m/%Y") 
    report_time = datetime.now().strftime("%H:%M:%S")
    #Calls findIndex to setup the Unique ID for that report.
    UID = topic+str(findIndex(topic))
    #Sets the data
    #URL Name is the image URL from cloudinary
    #Set the rest to empty as its only needed after we close an incident
    data = {
        "Id": UID,
        "Topic": topic,
        "date": report_date,
        "time": report_time,
        "Description": description,
        "Report_Status": True,
        "urlImg": urlName, 
        "ReasonForClosure": "", 
        "AdditionalInfo": "",
        "ClosureDateTime": ""
    }
    #If sucessfully it'll send out a telegram notification & saves report in the firebase
    try:
        fireDatabase.child("Reports").child(topic).child(UID).set(data)
        teleNotification("Incident Report has been created please do check the website UID: " + UID + "\n\n" + urlName)
    except Exception as e:
        print("Error occurred while creating the report:", e)

