<?php
set_time_limit(600); // Set the maximum execution time to 600 seconds (10 minutes)
$taValue = ""; // Initialize the variable with an empty string
$responseMsg = "";
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["btnClear"])) {
    $taValue = "";
  }

if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["btnSubmit"])) {
    // Assuming you have a function to handle the form data and communicate with the Flask server
    $inputText = $_POST['textAreaChatbot'];
    $response = sendDataToFlaskServer($inputText);
    // Process the response from the Flask server as needed
    $responseMsg = $response['result'];
}

//Sends out the input to the flask server
function sendDataToFlaskServer($inputText) {
    $data = array(
        'inputText' => $inputText,
    );

    $jsonData = json_encode($data);
    $flaskServerUrl = 'http://127.0.0.1:8080/chatbot';

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $flaskServerUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_TIMEOUT, 600); // Set the timeout to 30 seconds (adjust as needed)
    $response = curl_exec($ch);
    curl_close($ch);

    if ($response === false) {
        $error_message = 'Failed to connect to the Flask server.';
        return array('error' => $error_message);
    }

    $decodedResponse = json_decode($response, true);
    return $decodedResponse;
}


?>

<html>
<head>
    <title>Chatbot</title>
    <!-- Spinning Loader CSS -->
    <style>
        .loader {
            border: 4px solid rgba(0, 0, 0, 0.3);
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
            margin-top: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<link rel="stylesheet" type="text/css" href="..\style\mainPageStyle.css">

<body class="mainPageContainer">
    <?php include "navPartialView.php"; ?>
    <div id="tableContainer">
        <div id="chatContainer">
            <h1>Chatbot</h1>
            <img src="image\wall-e.jpg" width="150" height="270"> 

            <div id="labelDolly">
              <label>Ask Dolly</label>
            </div>
        
            <form method="POST">
                <textarea placeholder=" What would you like to know?" name="textAreaChatbot"><?php echo $taValue; ?></textarea>
                <div id="chatBtnContainer">
                    <button type="submit" name="btnClear">Clear</button>
                    <button type="button" id="btnSpeech">Microphone</button> 
                    <button type="submit" name="btnSubmit">Submit</button>
                </div>
            </form>

            <!-- Display the loading spinner -->
            <div id="loadingSpinner" style="display: none;">
                <div class="loader"></div>
                <p>Loading...</p>
            </div>

            <!-- Display the response message here -->
            <div id="responseMessage">
                <p><?php echo $responseMsg; ?></p>
                <?php if ($responseMsg != null): ?>
                    <style>
                        #loadingSpinner {
                            display: none;
                        }
                        #responseMessage {
                            display: block;
                        }
                    </style>
                <?php endif; ?>
            </div>
        </div>
    </div>
<script src="chatbot.js"></script>
</body>
</html>
