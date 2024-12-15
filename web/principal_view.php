<?php
session_start();
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Verify if the session contains the expected data
if (!isset($_SESSION['S_idEstudiant']) || !isset($_SESSION['S_Nom'])) {
    echo "La sesión no está configurada correctamente. Redirigiendo a login.html.";
    header("Location: /login.html");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Principal View</title>
    <link rel="stylesheet" href="style_web.css">
</head>
<body>
    <div class="main-container">
        <h1>Welcome to ATENEA_PBE dear <?php echo $_SESSION['S_Nom']; ?> !</h1>
        
	<!-- Wron talbe print -->
	<?php
        if (isset($_SESSION['errorTable']) && $_SESSION['errorTable'] === true) {
            echo "<p style='color: red;'>Table Error, try again please with a valid table.</p>";
            // Clear the boolean value to avoid displaying it again
            unset($_SESSION['errorTable']);
        }
        ?>
	<!--Search form-->
        <form class="search-form" action="/filtres.php" method="GET">
            <input type="text" name="table" placeholder="Enter table (for example, marks)" required>
            <input type="text" name="filter" placeholder="Enter Filter (for example, mark[gt]=5)">
            

        <button class="search-button" type="submit">Search</button>
        <button class="logout-button" onclick="location.href='login.html'">Logout</button>
        </form>

        <!-- Show results -->
        <?php
        if (isset($_SESSION['S_result'])) {
            $resultados = json_decode($_SESSION['S_result'], true);

            if (!empty($resultados)) {
                echo "<table border='1'>";
                echo "<thead>";
                foreach (array_keys($resultados[0]) as $columna) {
                    echo "<th>$columna</th>";
                }
                echo "</thead>";
                echo "<tbody>";
                foreach ($resultados as $fila) {
                    echo "<tr>";
                    foreach ($fila as $valor) {
                        echo "<td>$valor</td>";
                    }
                    echo "</tr>";
                }
                echo "</tbody>";
                echo "</table>";
            } else {
                echo "<p>No results found.</p>";
            }

            //Clear the session to avoid duplicate results
            unset($_SESSION['S_result']);
        }
        ?>
    </div>
</body>
</html>         
