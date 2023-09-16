# Pokemon 2
`Clone2Own`
This is a pretty cool project, but we don't care about that - we only want flags. We can see that there's a few places were the source code writes to files:
```php
index.php
180:    file_put_contents("save/$username.txt", implode("|", $userData));
265:    file_put_contents("save/$username/$username.txt", implode("|", $userData));
```
Initially I thought that we might be able to do some sort of path traversal here, because what if we gave a username with `../` in it. Let's look at one of these files:
```
Bamuel|c43e5ca186e83c1831054ad12b78126f4541f6c85d831b9eb5cb073c4d026571638312c6ae4fba4dbbb7158df4906fb95850c7ddd9589ea24b83a1cb009b2696|Male|175|a|26/09/2016|3%
```
Cool so it seems that the first part is the username, then there's some password hash, gender, and other stuff. I wonder what this is used for? Let's look at references to `save/` we find in the `admin2.php` file:
```php
$dir = "save/";
// Sort in ascending order
$a = scandir($dir);
foreach($a as $user) {
    $users = str_replace('.txt', '', $user);
    $userlist = file ('save/'. $users . '/' . $users . '.txt');
    foreach ($userlist as $user2) {
        $user_details = explode('|', $user2);
        $username2 = $user_details[0];
        $password = $user_details[1];
        $gender = $user_details[2];
        $step = $user_details[3];
        $premiumuser = $user_details[4];
        $startdate = $user_details[5];
        $idnumber = $user_details[6];
        $admin2 = $user_details[7];
        $idnumber2 = sprintf("%08d", $idnumber);
```
We see that it has `admin2` field, which tells whether the user is admin. We see in `index.php`
```php
if ($admin == "admin"){
//    ADMIN PAGE
    echo "<a href=\"admin2.php\"><button class=\"btn-1\" style=\"float:left;\">Admin login</button></a><br>";
}
```
So can we control this field? Well what if we take could send a username like:
`||||admin`. What I did was I intercepted the `save` command on the site and changed my amount of steps to something like: `10|b|b|b|admin`, and then you get the flag!

Flag:
`TDCNET{PHPikachu_XD_Vildt_sagt_hestenettet}`