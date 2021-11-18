<?php

include('db.php');
$ip = $_SERVER['REMOTE_ADDR'];
$consulta="SELECT*FROM usuarios where IP='$ip'";
$resultado = mysqli_query($conexion,$consulta);

$filas=mysqli_num_rows($resultado);

if ($filas){
	foreach ($_FILES['archivo']['tmp_name'] as $key => $tmp_name) {
		if ($_FILES['archivo']['name'][$key]) {
			$filename = $_FILES['archivo']['name'][$key];
			$temporal = $_FILES['archivo']['tmp_name'][$key];

			$directorio = $ip;

			if (!file_exists($directorio)) {
				mkdir($directorio, 0777, true);
			}

			$dir = opendir($directorio);
			$ruta = $directorio.'/'.$filename;

			if (move_uploaded_file($temporal, $ruta)) {
				header('Location: index.html');

			} else{
				json_output(400,"Hubo un error");
			}
		closedir($dir);
		}
	}
	// header('Location: index.html');
}else{
	?>
	<?php
	include('index.html');
	?>
	<h1 class="bad">ERROR EN LA AUTENTIFICACION</h1>
	<?php
}
mysqli_free_result($resultado);
mysqli_close($conexion);



?>
