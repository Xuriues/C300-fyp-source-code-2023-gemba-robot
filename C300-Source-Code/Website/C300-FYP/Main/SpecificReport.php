<?php
include("db/dbconfig.php");
include("db/firebase.php");

$db = new firebaseRDB($dbURL);

$reportID = $_GET['reportID'];

$data = $db->retrieve("Reports");
$data = json_decode($data, true);
$foundReport = null;
$errorMsg = "Report Details Of $reportID";
foreach ($data as $topic => $reports) {

		foreach ($reports as $report) {
			if ($report['Id'] === $reportID) {
				$foundReport = $report;
				break;
			}
		}
	}

if (!$foundReport) {
	$errorMsg = "Unable to find record.";
} 

?>

<html>
<head>
  <title>Report Details</title>
</head>
<link rel="stylesheet" type="text/css" href="..\style\mainPageStyle.css">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<script type="text/javascript">
	$(document).ready(function() {
	$("select").on("click" , function() {
  
  $(this).parent(".select-box").toggleClass("open");
  
});

$(document).mouseup(function (e)
{
    var container = $(".select-box");

    if (container.has(e.target).length === 0) {
        container.removeClass("open");
    }
});


$("select").on("change" , function() {
  
  var selection = $(this).find("option:selected").text(),
      labelFor = $(this).attr("id"),
      label = $("[for='" + labelFor + "']");
    
  label.find(".label-desc").html(selection);
    
	});
});

function GoBackWithRefresh(event) {
    if ('referrer' in document) {
        window.location = document.referrer;
    } else {
        window.history.back();
    }
}
</script>
<body class="mainPageContainer">

	<?php include "navPartialView.php"; ?>
		<div id="tableContainer">
		<?php
			$urlImg = $foundReport["urlImg"];
			//echo "<img src='$urlImg'>"
		?>
		<h1 style="margin-left:20px">Report Details</h1>
		<form method="POST" action="UpdateReportFunc.php">
    <input type="hidden" name="foundReport" value="<?php echo htmlspecialchars(json_encode($foundReport)); ?>">

				<div class="image-container">
					<img src="<?php echo $urlImg; ?>" style="width: 500px; height: 500px;"> 
					<div class="label-container">
						<div>
							<label> <?php echo $errorMsg; ?> </label>
						</div>
						<div>
							<label>Date Of Incident: <?php echo $foundReport["date"]; ?> </label>
						</div>
						<div>
							<label>Time Of Incident: <?php echo $foundReport["time"]; ?> </label>
						</div>
						<div>
							<label>Description: <?php echo $foundReport["Description"]; ?> </label>
						</div>
						<?php 
								if ($foundReport["ReasonForClosure"] != null) {
									
										echo "<div>"; 
									 	echo "<label>Reason for closure: " . $foundReport["ReasonForClosure"] ."</label>";
										echo "</div>";

										echo "<div>"; 
									 	echo "<label>Date & Time of Closure: " . $foundReport["ClosureDateTime"] ."</label>";
										echo "</div>";
								}
								else {
									echo '
										<div class="select-box">
										    <label for="select-box1" class="label select-box1" style="font-size: 19px;">
										        <span class="label-desc">Reason for Closure</span>
										    </label>
										    <select id="select-box1" class="select" name="reasonForClosure">
										        <option disabled selected>Select an option</option>
										        <option value="Incident resolved">Incident resolved</option>
										        <option value="False Detection">False Detection</option>
										        <option value="Repeated Entry">Repeated Entry</option>
										    </select>
										</div>';
								}
              ?>
						<div>
							<div><label>Additional Notes for closure:</label></div>
							<textarea id="incidentTextArea" name="textAreaReport" <?php if (!$foundReport["Report_Status"]) { echo "disabled"; } ?>><?php if (!$foundReport["Report_Status"]) { echo $foundReport["AdditionalInfo"]; } ?></textarea>
						</div>
						<div class="reportPageBtnContainer">
							<?php 
								 if ($foundReport["Report_Status"]) {
								 		echo "<input type='submit' value='Close Incident'>";
								}
							?>
							<a href="javascript:void(0);" onclick="goBack()">
							   
							</a>
							<a href="#" onclick="GoBackWithRefresh();return false;"> 
								<input type="button" value="Back">
							</a>
						</div>		
					</div>
				</div>
			</form>
</body>
</html>
