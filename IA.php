<?php

// $ip = $_SERVER['REMOTE_ADDR'];
$remote = isset($_SERVER["REMOTE_ADDR"]) ? $_SERVER["REMOTE_ADDR"] : '127.0.0.1';
$python = system("C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python.exe IA.py .$remote");

//echo //'<script language="javascript">alert("juas");</script>';
// header('Location: index.html');
// echo $python;
 //echo '
//  </pre>

 //<hr />Ultima linea de la salida: ' . $python . '

// <hr />Valor de retorno: ' . $retval;

?>