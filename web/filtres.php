<?php
session_start();
ini_set('display_errors', 1);
error_reporting(E_ALL);

header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Content-Type: application/json');

include("database.php");

//Extract the table from the GET parameter
$table = isset($_GET['table']) ? $_GET['table'] : null;
$filterString = isset($_GET['filter']) ? $_GET['filter'] : null;
$uid = $_SESSION['S_idEstudiant'];

$allowedTables = ['marks', 'tasks', 'timetables', 'students'];
if (!$table || !in_array(strtolower($table), $allowedTables)) {
    http_response_code(400);
    $_SESSION['errorTable']= true;
    echo "ERROR: Tabla no válida";
    header("Location: principal_view.php");
    exit;
}

// inizialization
$query = "SELECT * FROM `$table`";
$whereConditions = [];

// Process filters
$queryParams = [];
if ($filterString) {
    parse_str($filterString, $queryParams);
    $_SESION['errortabla']= false;
    foreach ($queryParams as $field => $conditions) {
        if ($field === 'limit') {
            $limit = intval($conditions);
            continue;
        }

        if (is_array($conditions)) {
            foreach ($conditions as $operator => $value) {
                $value = $mysqli->real_escape_string($value);
                $value = "'$value'";
                switch ($operator) {
                    case 'lt':  $whereConditions[] = "`$field` < $value"; break;
                    case 'lte': $whereConditions[] = "`$field` <= $value"; break;
                    case 'gt':  $whereConditions[] = "`$field` > $value"; break;
                    case 'gte': $whereConditions[] = "`$field` >= $value"; break;
                    case 'eq':  $whereConditions[] = "`$field` = $value"; break;
                }
            }
        } else {
            $value = $mysqli->real_escape_string($conditions);
            $whereConditions[] = "`$field` = '$value'";
        }
    }
}

if ($table === 'marks') {
    $whereConditions[] = "`uid` = '$uid'";
}

// Construct WHERE clause if conditions exist
if (!empty($whereConditions)) {
    $query .= " WHERE " . implode(' AND ', $whereConditions);
}

if (isset($limit)) { // Add limit if necessary
    $query .= " LIMIT $limit";
}

// Excecute the quey
$result = $mysqli->query($query);

if ($result) {
    $data = $result->fetch_all(MYSQLI_ASSOC);

    // Save results in session and redirect back to principal_view.php
    $_SESSION['S_result'] = json_encode($data);
    header('Location: /principal_view.php');
    exit;
} else {
    http_response_code(500);
    echo json_encode([
        'error' => 'Database query failed',
        'details' => $mysqli->error
    ]);
}

$mysqli->close();
?>
