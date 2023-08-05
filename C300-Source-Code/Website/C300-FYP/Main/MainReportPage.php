<?php
include("db/dbconfig.php");
include("db/firebase.php");

$db = new firebaseRDB($dbURL);
?>

<html>
<head>
  <title>Reports</title>
</head>
<link rel="stylesheet" type="text/css" href="..\style\mainPageStyle.css">
<body class="mainPageContainer">
	<?php include "navPartialView.php"; ?>
	<div id="tableContainer">
		<h1 style="margin-left:15px">Overall Reports</h1>
		<?php
			$data = $db->retrieve("Reports");
			$data = json_decode($data, true);
			if (empty($data)) {
				echo "<p>No reports to display.</p>";
			} else {
				echo "<table>";
				echo "<tr>";
				echo "<th>ReportID</th>";
				echo "<th>Topic</th>";
				echo "<th>Date & Time</th>";
				
				echo "<th>Status</th>";
				echo "<th></th>";
				echo "</tr>";
				
				foreach ($data as $topic => $reports) {
					foreach ($reports as $report) {
						$reportID = $report["Id"];
						$topic = $report["Topic"];
						$date = $report["date"];
						$date = str_replace('/', '-', $date); 
						$time = $report["time"];

						$formatTime = date('h:i:s A', strtotime($time));
						$formatDate = date('d M Y', strtotime($date));
						$status = $report["Report_Status"];
						

						echo "<tr>";
						echo "<td>$reportID</td>";
						echo "<td>$topic</td>";
						echo "<td>$formatDate &emsp; $formatTime</td>";
						

						if ($status == true) {
								echo "<td id='onGoing'>Pending</td>";
						}
						else {
								echo "<td id='close'>Resolved</td>";
						}
						
						echo "<td><a href='SpecificReport.php?reportID=$reportID'><input type='button' value='View' class='tableBtn'></a></td>";
						echo "</tr>";
					}
				}
				
				echo "</table>";
			}
		?>
	</div>
</body>
</html>