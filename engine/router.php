<?php
// Router for `php -S`: serve real files directly, send everything else to WordPress.
$path = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $_SERVER['DOCUMENT_ROOT'] . $path;
if ($path !== '/' && is_file($file) && substr($file, -4) !== '.php') {
    return false;
}
if ($path !== '/' && is_file($file)) {          // wp-login.php, wp-admin/*.php
    chdir(dirname($file));
    $_SERVER['SCRIPT_NAME'] = $path;
    $_SERVER['SCRIPT_FILENAME'] = $file;
    require $file;
    return;
}
if (is_dir($file) && is_file(rtrim($file, '/') . '/index.php')) {   // /wp-admin/
    chdir($file);
    $_SERVER['SCRIPT_NAME'] = rtrim($path, '/') . '/index.php';
    require rtrim($file, '/') . '/index.php';
    return;
}
$_SERVER['SCRIPT_NAME'] = '/index.php';
$_SERVER['SCRIPT_FILENAME'] = $_SERVER['DOCUMENT_ROOT'] . '/index.php';
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
