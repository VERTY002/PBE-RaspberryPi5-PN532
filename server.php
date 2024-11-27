
#primer programa per part del servidor 
#actualment no funciona com hauria de funcionar, no hem pogut comprobar el correcte funcionament del codi ja que té 
#errors i no es connecta amb el client entre altres coses.

<?php 
include ("database.php"); // incluimos la funcion conn

$request= explode('/',$_SERVER['REQUEST_URI']); 
// request_uri lo que hace es quedarse con lo importante para nosotros
// explode lo que hace es separar la cadena de texto por '/', es un array
$request= array_filter($request); // array_filter lo que hace es filtrar, es decir lo que es nulo, 0, false lo elimina.
$request= end($request); // end lo que hace es devolver el ultimo elemento de la cadena de texto.
$request= explode('?',$request);

switch($request[0]){ // request[0] lo que hace es que nos devuelva el primer elemento del array, lo que tenemos en nuestro caso es lo que quiere que le devolvamos 
  case 'uid':
    if(isset($_SERVER['HTTP_UID'])){ 
      //nos devuelve el uid del estudiante, comprobamos si existe
      $uid=$_SERVER['HTTP_UID']; // lo guardamos en una variable 
      $consulta="Select name from students where password='$uid'";
      // seleccionamos solo el nombre del estudiante por su uid, que es el password en nuestra base de datos.
    }
  break;
  case 'timetables':
    $consulta="Select * from timetables"; // la consulta tiene que devolver toda la lista de timetables.
    if(isset($_GET['day'])){
       $day=$_GET['day']; // miramos siempre primero si existe porque puede haber un error de asignacion de variable en caso de que no exista.
       $consulta .="WHERE day='$day'"; // que ponga solo en la lista los que el dia coincida.
       if(isset($_GET['hour'])){
         $hour=$_GET['hour'];
         $consulta .="AND hour='$hour'"; // lo mismo con la hora
       }
    }
    if(isset($_GET['limit'])){
      $limit= $_GET['limit'];
      $consulta .="LIMIT $limit"; // en caso de que indique limite se lo añadimos
    }
  break;
  case 'marks':
    if(isset($_SERVER['HTTP_UID'])){
      $uid=$_SERVER['HTTP_UID'];
      $consulta= "SELECT subject,name,mark FROM marks WHERE uid='$uid'";
    }
    if(isset($_GET['subject'])){
      $subject=$_GET['subject'];
      $consulta .="AND subject='$subject'";
    }
    if(isset($_GET['mark']['lt'])){ //lt es menor, en este caso es devolver los menores que la nota que le indicas
      $mark=$_GET['mark']['lt'];
      $consulta .="AND mark < '$mark'";
    }else if (isset($_GET['mark']['gt'])){ // gt es mayor, en este caso devolver los mayores que la nota que le indicas
      $mark=$_GET['mark']['gt'];
      $consulta .="AND mark > '$mark'";
    }
  break;
  case 'tasks':
      $consulta="Select * from tasks";
      if(isset($_GET['date'])){
        $date=$_GET['date'];
        if($date='now'){
          $consulta .="WHERE date= CURRENT_DATE"; // current date es la data actual
        } else{
          $consulta.="WHERE date= '$date'";
        }
      }
      $consulta .="ORDER BY date";
      if(isset($_GET['limit'])){
        $limit=$_GET['limit'];
        $consulta .="LIMIT $limit";
      }
      break;
  default: 
    echo "Error 404";
    exit();
}
$resultado=mysql_query($conn, $consulta); // ejecuta la query
$info=array();
while ($fila=mysql_fetch_assoc($resultado)){
  $info[]=$fila; // guardamos en un array la fila
}
header('Content-Type: application/json'); // le decimos que el formato va a ser json
echo json_encode($info); // le enviamos la informacion al cliente en json
?>

