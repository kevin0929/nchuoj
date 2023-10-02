<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>馬停偉助教</title>
</head>

<body>
    <?php
    session_start();
    if($_SESSION["login_session"] != true)
        header("Location: index.html");
    ?>
    <table width=40% border=1 align=center>
        <tr>
            <td align=center>
                <b><a href=summer_class.php> 2021暑期先修班 </a></b>
            </td>
        </tr>
        <tr>
            <td align=center>
                <b><a>  </a></b>
            </td>
        </tr>
    </table>
</body>
</body>