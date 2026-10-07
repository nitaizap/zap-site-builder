<?php
/**
 * Zap client site. Fill the four DB_ values (deploy.sh does it for you).
 */
define('DB_NAME', '__DB_NAME__');
define('DB_USER', '__DB_USER__');
define('DB_PASSWORD', '__DB_PASSWORD__');
define('DB_HOST', '__DB_HOST__');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

{{SALTS}}

$table_prefix = 'wp_';

define('WP_ENVIRONMENT_TYPE', '{{ENV}}');
define('DISALLOW_FILE_EDIT', true);
define('WP_POST_REVISIONS', 5);
define('WP_DEBUG', false);
define('WP_DEBUG_LOG', false);
define('WP_DEBUG_DISPLAY', false);
define('FORCE_SSL_ADMIN', true);
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
