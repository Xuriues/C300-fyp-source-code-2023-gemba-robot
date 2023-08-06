<!-- Main page for the user to try out the AI models from the back end. Done by Kezia -->
<!DOCTYPE html>
<html>
<head>
    <title>AI Integration Page</title>
    <!-- Include jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<link rel="stylesheet" type="text/css" href="..\style\mainPageStyle.css">
<body class="mainPageContainer">
    <?php include "navPartialView.php"; ?>
    <div id="tableContainer">
        <h1 style="margin-left:15px">AI Integration</h1>
            <a href="http://127.0.0.1:8080/?data=loadPPE"> <button class="AIModelButton">Load PPE</button></a>
            <a href="http://127.0.0.1:8080/?data=loadBoxes"> <button class="AIModelButton">Load Boxes</button></a>
            <a href="http://127.0.0.1:8080/?data=loadMHE"> <button class="AIModelButton">Load MHE</button></a>
    </div>
</body>
</html>