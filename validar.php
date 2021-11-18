<?php
	$usuario = $_POST['usuario'];
	$contrasena = $_POST['contrasena'];
	session_start();
	$_SESSION['usuario']=$usuario;

	include('db.php');

	$consulta="SELECT*FROM usuarios where usuario='$usuario' and contrasena='$contrasena'";
	$resultado = mysqli_query($conexion,$consulta);

	$filas=mysqli_num_rows($resultado);

	if ($filas){
		header('Location: index.html');
	}else{
		?>
		<?php
		include('index.php');
		?>
		<h1 class="bad">ERROR EN LA AUTENTIFICACION</h1>
		<?php
	}
	mysqli_free_result($resultado);
	mysqli_close($conexion);
?>