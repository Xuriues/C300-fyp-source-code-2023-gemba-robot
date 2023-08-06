<?php
// Include this 2 files to work with firebase.
include("db/dbconfig.php");
include("db/firebase.php");
//Retrieves the DB URL specified in the db folder.
$db = new firebaseRDB($dbURL);
?>

<html>
<head>
  <title>MHE Detection</title>
</head>
<link rel="stylesheet" type="text/css" href="..\style\mainPageStyle.css">
<body class="mainPageContainer">
	<?php include "navPartialView.php"; ?>
	<div id="tableContainer">
		<h1 style="margin-left:15px">MHE Detection</h1>
		<?php
			$data = $db->retrieve("Reports");
			$data = json_decode($data, true);
			if (empty($data)) {
				echo "<p>No Reports to show</p>";
			}
			else {
				$hasReports = false; // Flag variable
				echo "<table>";
				echo "<tr>";
				echo "<th>ReportID</th>";
				echo "<th>Date & Time</th>";
				echo "<th>Status</th>";
				echo "</tr>";
				
				foreach ($data as $topic => $reports) {
					if ($topic === "MHE") {
						foreach ($reports as $report) {
							$reportID = $report["Id"];
							$date = $report["date"];
							$date = str_replace('/', '-', $date); 
							$time = $report["time"];

							$formatTime = date('h:i:s A', strtotime($time));
							$formatDate = date('d M Y', strtotime($date));
							$status = $report["Report_Status"];
							echo "<tr>";
							echo "<td>$reportID</td>";
							echo "<td>$formatDate &emsp; $formatTime</td>";

							if ($status == true) {
									echo "<td id='onGoing'>Pending</td>";
							}
							else {
									echo "<td id='close'>Resolved</td>";
							}
							echo "<td><input type='button' value='View' class='tableBtn' onclick=\"location.href='SpecificReport.php?reportID=$reportID'\"></td>";
							echo "</tr>";
							$hasReports = true;
						}
						echo "</table>";
					}
				}
				if (!$hasReports) {
					echo "<p>No Reports in the Boxes category</p>";
				}
			}
		?>
	</div>
</body>
</html>
