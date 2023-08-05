<!-- Inside updateReport.php -->
<?php
include("db/dbconfig.php");
include("db/firebase.php");

$db = new firebaseRDB($dbURL);

if (isset($_POST['foundReport'])) {
    $foundReport = json_decode($_POST['foundReport'], true);
    $reasonForClosure = $_POST['reasonForClosure'];
    $incidentNotes = $_POST['textAreaReport'];

    $options = array("Incident resolved", "False Detection", "Repeated Entry");
    $flag = false;
    foreach ($options as $option) {
        if ($reasonForClosure == $option) {
            $flag = true;
            break;
        }
    }
    if (!$flag) {
        $id = $foundReport['Id'];
        echo "<script>alert('Please pick an option.'); window.location.href = 'SpecificReport.php?reportID=$id';</script>";
        exit();
    }

    $updateData = [
        "Id"    => $foundReport['Id'],
        "Topic" => $foundReport['Topic'],
        "date"  =>  $foundReport['date'],
        "time"  =>  $foundReport['time'],
        "Description" =>  $foundReport['Description'],
        "Report_Status" =>  False,
        "urlImg" => $foundReport['urlImg'],
        "ReasonForClosure" =>  $reasonForClosure,
        "AdditionalInfo" =>  $incidentNotes
    ];
    $pathName = "Reports/" . $foundReport['Topic'];

    $updateResult = $db->update($pathName, $foundReport['Id'], $updateData);

    if ($updateResult) {
        $alertMessage = $foundReport['Id'] . " has been closed.";
    } else {
        // If the update failed, you can handle the error here
        $alertMessage = "Failed to update the report.";
    }
    
    $id = $foundReport['Id'];
    echo "<script>alert('$alertMessage'); window.location.href = 'MainReportPage.php';</script>";

    exit();

} else {
    echo "Error: Unable to find report";
}
?>