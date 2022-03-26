<?php

    include 'getdata.php';

    

?>




<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Map</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/Footer-Basic.css">
    <link rel="stylesheet" href="assets/css/Navigation-with-Button-1.css">
    <link rel="stylesheet" href="assets/css/Navigation-with-Button.css">
    <link rel="stylesheet" href="assets/css/styles.css">
    <link rel="stylesheet" href="assets/css/Team-Clean.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>

    <script>

        
    </script>
</head>

<body>
    <nav class="navbar navbar-light navbar-expand-lg navigation-clean-button" style="background: #000000;">
        <div class="container"><a class="navbar-brand" href="#" style="color: white;pointer-events: none;">aiAgro</a><button data-bs-toggle="collapse" class="navbar-toggler" data-bs-target="#navcol-1" style="border-width: 2px;"><span class="visually-hidden">Toggle navigation</span><span class="navbar-toggler-icon" style="filter: invert(100%) saturate(0%) sepia(0%);"></span></button>
            <div class="collapse navbar-collapse" id="navcol-1">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link active" href="index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#" style="color: white;pointer-events: none;">Map</a></li>
                    <li class="nav-item"><a class="nav-link" href="info.html" style="color: white;">Info</a></li>
                </ul><span class="navbar-text actions"> </span>
            </div>
        </div>
    </nav>
    <div class="container">
        <div class="row" style="margin-top: 50px;">
            <div class="col-md-6" id="map" style="height: 391.28px;width: 476px;border-width: 0px;border-style: solid;"></div>
            <div class="col-md-6" style="width: 476px;height: 391.28px;border-width: 0px;border-style: solid;margin-left: 6px;">
                <ul></ul>
                <div class="table-responsive" style="width: 392px;">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th style="text-align: left;">Values</th>
                            </tr>
                        </thead>
                        <tbody>
                            
                            <?php
                                $rayonName = $_GET["uid"];
                                $sql = "SELECT * FROM hackathondata WHERE Rayon = '" . $rayonName . "'";
                                $result = mysqli_query($conn, $sql);
                                if (mysqli_num_rows($result) > 0){
                                    while ($row = mysqli_fetch_assoc($result)) {
                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Region";
                                        echo "</td>";
                                        echo '<td id="rayon">';
                                        echo $row['Rayon'];
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "River level (today)";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['RiverLevelToday'] . " m";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Monthly average river level";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['AvgLevelSeason'] . " m";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Rain fall (next week)";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['RainFallNextWeek'] . " mm";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Rain fall (in 2 weeks)";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['RainFallSecondWeek'] . " mm";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Estimated river level (in 3 weeks)";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['Prediction'] . " m";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Max. river level";
                                        echo "</td>";
                                        echo "<td>";
                                        echo $row['LevelLimit'] . " m";
                                        echo "</td>";
                                        echo "</tr>";

                                        echo "<tr>";
                                        echo "<td>";
                                        echo "Risk of flood";
                                        echo "</td>";
                                        echo "<td>";
                                        echo '<div class="progress" style="transform: translateY(5px);">';
                                        echo '<div class="progress-bar" aria-valuenow="' . $row['FloodProbability'] .  '" aria-valuemin="0" aria-valuemax="100" style="width:' . $row['FloodProbability'] . '%;"><span class="visually-hidden"></span></div>';
                                        echo "</div>";
                                        echo "</td>";
                                        echo "</tr>";
                                    }
                                }
                                else{
                                    echo $rayonName;
                                }
                            ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <footer class="footer-basic" style="margin-top: 50px;">
        <ul class="list-inline">
            <li class="list-inline-item"><a href="index.html" style="pointer-events: auto;">Home</a></li>
            <li class="list-inline-item"><a href="info.html">Info</a></li>
            <li class="list-inline-item"><a href="#">Terms</a></li>
            <li class="list-inline-item"><a href="#">Privacy Policy</a></li>
        </ul>
        <p class="copyright">aiAgro © 2022</p>
    </footer>
    <script src="assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="assets/js/bs-init.js"></script>
    <script src="assets/js/countrymap.js"></script>
    <script src="assets/js/index.js"></script>
    <script src="assets/js/mapdata.js"></script>
</body>

</html>