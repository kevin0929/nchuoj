<?php
session_start();
$username = ""; $password = "";

if( isset($_POST["username"]) )
    $username = $_POST["username"];
if( isset($_POST["password"]) )
    $password = $_POST["password"];

if($username != "" && $password != "")
{
    $link = mysqli_connect("localhost","root","mysql11581158","User") or die("無法開啟MySQL資料庫連接!<br/>");
    mysqli_query($link, 'SET NAMES utf8');

    $sql = "SELECT * FROM 學生名單 WHERE password='";
    $sql.= $password."' AND username='".$username."'";
    echo $name;
    echo $password;

    $result = mysqli_query($link, $sql);
    $total_records = mysqli_num_rows($result);

    if($total_records > 0)
    {
        $_SESSION["login_session"] = true;
        header("Location: Teacher.html");
    }
    
    else
    {
        echo "<center><font color='white'>";
        echo "使用者名稱或密碼錯誤!<br/>";
        echo "</font>";
        $_SESSION["login_session"] = false;
    }
    mysqli_close($link);
}
