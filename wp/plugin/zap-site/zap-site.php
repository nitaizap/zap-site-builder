<?php
/**
 * Plugin Name: Zap Site
 * Description: Zap Group client-site standards: lead form (saved + emailed), SMTP relay, LocalBusiness/FAQ/Service schema, reviews widget, hardening.
 * Version: 1.0.0
 * Author: Zap Group
 * Requires PHP: 8.0
 * Text Domain: zap-site
 */
defined('ABSPATH') || exit;

const ZAP_SITE_VER = '1.0.0';

function zap_opt($key = null, $default = '') {
    if (function_exists('zs_opt')) return zs_opt($key, $default);
    $v = get_option('zap_site', []);
    if ($key === null) return $v;
    foreach (explode('.', $key) as $k) {
        if (!is_array($v) || !array_key_exists($k, $v)) return $default;
        $v = $v[$k];
    }
    return $v === null || $v === '' ? $default : $v;
}

require __DIR__ . '/inc/leads.php';
require __DIR__ . '/inc/schema.php';
require __DIR__ . '/inc/shortcodes.php';
require __DIR__ . '/inc/hardening.php';
require __DIR__ . '/inc/robots.php';
