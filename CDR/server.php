<?php
header('Access-Control-Allow-Origin: *');  
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
// Set the response header
header('Content-Type: application/json');
// Configuration of the database connection
include("database.php");

// Extract the table from the URL path
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$pathParts = explode('/', trim($path, '/'));
$table = end($pathParts);
 //Extract the uid from the URL path so we can show only the marks form the uid (privacy)
$uid=$pathParts[count($pathParts)-2];
// Validate the table name
$allowedTables = ['marks', 'tasks', 'timetables', 'students'];
if (!in_array(strtolower($table), $allowedTables)) {
    http_response_code(400);
    die(json_encode(['error' => 'Invalid table name']));
}

// Initialize the base query (mariaDB syntaxis)
$query = "SELECT * FROM `$table`";
$whereConditions = [];

// Analyze the query parameters
$queryString = parse_url($_SERVER['REQUEST_URI'], PHP_URL_QUERY);
$queryParams = [];
if ($queryString) {
    parse_str($queryString, $queryParams);
}

// Process filters and control parameters
$limit = null; // To store the value of limit, if it exists

foreach ($queryParams as $field => $conditions) {
    if ($field === 'limit') {
        // Processing the LIMIT parameter
        $limit = intval($conditions); // Convert to integer
        continue; // Jump to the next parameter
    }

    if (is_array($conditions)) {
        foreach ($conditions as $operator => $value) {
            if ($value === 'now') {
                $value = 'CURDATE()'; // Replace 'now' with MySQL function 
            } else {
                $value = $mysqli->real_escape_string($value); 
                $value = "'$value'"; // add '' to literal values
            }

            switch ($operator) {
                case 'lt':  $whereConditions[] = "`$field` < $value "; break;
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

if($table=='marks'){
    $whereConditions[] =" uid = '$uid'";
}

if (!empty($whereConditions)) {
    $query .= " WHERE " . implode(' AND ', $whereConditions);

}

if ($limit !== null) {
    $query .= " LIMIT $limit";
}

// Run query
$result = $mysqli->query($query);

if ($result) {
    // Obtain results
    $data = $result->fetch_all(MYSQLI_ASSOC);

    // Error log to see if there are any erros 
    error_log("Retrieved data: " . print_r($data, true));

    // JSON response
    echo json_encode($data, JSON_PRETTY_PRINT);
} else {

    http_response_code(500);
    error_log("Query error: " . $mysqli->error);
    echo json_encode([
        'error' => 'Database query failed',
        'details' => $mysqli->error
    ]);
}
$mysqli->close();
?>

