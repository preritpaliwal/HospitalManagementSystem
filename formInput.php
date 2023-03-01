<?php
    $f = $_POST['fn'];
    $l = $_POST['ln'];

    $conn = new mysqli('localhost','root','Mysql@123','20CS10046');
    if($conn->connect_error){
        die('connection failed: '.$conn->connect_error);
    }
    else{
        $stmt = $conn->prepare("insert into names values(?,?)");
        $stmt->bind_params("ss",$f,$l);
        $stmt->execute();
        echo "Registeration Successful...";
        $stmt->close();
        $conn->close();
    }
?>