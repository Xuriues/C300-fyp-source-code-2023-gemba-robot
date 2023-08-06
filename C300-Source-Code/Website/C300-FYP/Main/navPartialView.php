<?php
//Navigation page for the user to view reports, chatbot, & the AI.
$current_page = basename($_SERVER['PHP_SELF']);
?>
<div id="partialContainer">
  <a href="MainReportPage.php">
    <img src="image\mainPage_logov2.png" id="navLogo">
  </a>
  <div id="navContainer">
    <nav style="margin-top: 50px;">
      <ul>
        <li<?php if ($current_page === 'MainReportPage.php') echo ' class="active"'; ?>><a href="MainReportPage.php">Reports</a></li>
        <li<?php if ($current_page === 'MHEPage.php') echo ' class="active"'; ?>><a href="MHEPage.php">MHE Detection</a></li>
        <li<?php if ($current_page === 'PPEPage.php') echo ' class="active"'; ?>><a href="PPEPage.php">PPE Detection</a></li>
        <li<?php if ($current_page === 'BoxesPage.php') echo ' class="active"'; ?>><a href="BoxesPage.php">Boxes Detection</a></li>
        <li<?php if ($current_page === 'ChatbotPage.php') echo ' class="active"'; ?>><a href="ChatbotPage.php">Chatbot</a></li>
        <li<?php if ($current_page === 'AIModelPage.php') echo ' class="active"'; ?>><a href="AIModelPage.php">AI Model Integration</a></li>
        <li><a href="../Login/LoginPage.php">Logout</a></li>
      </ul>
    </nav>
  </div>
</div>
