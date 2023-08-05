<?php
include("dbconfig.php");
include("firebase.php");

$db = new firebaseRDB($dbURL);
?>

<table>
	<tr>
		<th>Description</th>
		<th>Id</th>
	</tr>

	<?php
		$data = $db->retrieve("Reports");
		$data = json_decode($data, 1);
		foreach ($data as $topic => $reports) {
    		foreach ($reports as $report) {
    			if ($report["Topic"] == "Boxes") {
					$description = $report["Description"];
			        $id = $report["Id"];
			        echo "<tr>";
			        echo "<td>$description</td>";
			        echo "<td>$id</td>";
			        echo "</tr>";
    			}
		    }
		}
	?>
	
</table>