<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if the userName and password fields are set
    if (isset($_POST["userName"]) && isset($_POST["password"])) {
        // Get the entered username and password
        $username = $_POST["userName"];
        $password = $_POST["password"];

        // Check against input
        if ($username == "admin" && $password == "admin") {
            // Perform the form action (redirect to homePage.php)
            header("Location: ..\Main\MainReportPage.php");
            exit; // Make sure to exit after the redirect
        } else {
            // Set the error message
            $errorMsg = "Invalid username or password.";
        }
    } else {
        $errorMsg = "Username and password are required.";
    }
}
?>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="..\style\loginStyle.css">
</head>
<title>
	Login
</title>
<body id="test">
<div class="loginContainer"> 
	<div class="logoContainer">
		<img src="..\Main\image\toll.png" width="150" height="150"> 
	</div>
	<form method="POST">
		<div id="inputContainer">
			<div class="inputItems">
				<label>Username</label>
				<input type="text" name="userName"/>
			</div>
			<div class="inputItems">
				<label>Password</label>
				<input type="password" name="password" />
			</div>
			<div id="submitContainer">
				<?php if (isset($errorMsg)) : ?>
                	<label class="errorMsg"><?php echo $errorMsg; ?></label>
            	<?php endif; ?>
				<input type="submit" id="btnSubmit" value="SIGN IN"/>
			</div>
		</div>
	</form>
</div>
</body>
</html>