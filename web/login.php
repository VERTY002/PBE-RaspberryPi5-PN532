<?php
session_start();
ini_set('display_errors', 1);
error_reporting(E_ALL);

include("database.php");

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    $username = $mysqli->real_escape_string($_POST['username']);
    $password = $mysqli->real_escape_string($_POST['password']);

    $sql = "SELECT * FROM students WHERE name='$username' AND uid='$password'";
    $result = $mysqli->query($sql);

    if ($result && $row = $result->fetch_assoc()) {
        // Save credentials
        $_SESSION['S_idEstudiant'] = $row['uid'];
        $_SESSION['S_Nom'] = $row['name'];
        

        // Redirect
        header("Location:/principal_view.php");
        exit;
    } else {
        // Redirect to error page 
        header("Location: /wrong_login.html");
        exit;
    }
} else {
    // Redirect to login 
    header("Location: /login.html");
    exit;
}
?>
