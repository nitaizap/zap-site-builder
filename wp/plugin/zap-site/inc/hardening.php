<?php
/** Baseline hardening that every Zap site ships with. Host-level items are on the launch checklist. */
defined('ABSPATH') || exit;

add_filter('xmlrpc_enabled', '__return_false');
add_filter('wp_headers', function ($h) { unset($h['X-Pingback']); return $h; });

/* No user enumeration: ?author=N and the public users endpoint. */
add_action('template_redirect', function () {
    if (!is_user_logged_in() && (isset($_GET['author']) || is_author())) {
        wp_safe_redirect(home_url('/'), 301);
        exit;
    }
});
add_filter('rest_endpoints', function ($e) {
    if (!is_user_logged_in()) {
        unset($e['/wp/v2/users'], $e['/wp/v2/users/(?P<id>[\d]+)']);
    }
    return $e;
});

/* Basic security headers (cached pages get them from the server config on launch). */
add_action('send_headers', function () {
    if (is_admin()) return;
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
});

/* Yoast: no debug comments in the HTML. */
add_filter('wpseo_debug_markers', '__return_false');
