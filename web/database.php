<?php
$host = 'localhost';
$username = 'root';
$password = 'telematik';
$database = 'atenea_pbe';

// Establecer la conexión a la base de datos
$mysqli = new mysqli($host, $username, $password, $database);
if ($mysqli->connect_error) {
    die(json_encode([
        'error' => 'Database connection failed',
        'details' => $mysqli->connect_error
    ]));
}
?>
