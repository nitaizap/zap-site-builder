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

// Zap SEO checklist: every image under 100 KB. The engine uploads light WebPs; keep WordPress's own resized copies light too.
add_filter('wp_editor_set_quality', fn() => 60);
// Detailed photos (HDR, foliage) can still pass 100 KB at 60: re-encode just those resized copies, lower each step.
add_filter('wp_generate_attachment_metadata', function ($meta, $id) {
    if (empty($meta['sizes']) || empty($meta['file'])) return $meta;
    $dir = trailingslashit(dirname(get_attached_file($id)));
    foreach ($meta['sizes'] as $name => $size) {
        $path = $dir . $size['file'];
        foreach ([50, 40, 32] as $q) {
            if (!is_file($path) || filesize($path) <= 100 * 1024) break;
            $ed = wp_get_image_editor($path);
            if (is_wp_error($ed)) break;
            $ed->set_quality($q);
            $saved = $ed->save($path);
            if (is_wp_error($saved)) break;
            clearstatcache(true, $path);
            $meta['sizes'][$name]['filesize'] = filesize($path);
        }
    }
    return $meta;
}, 20, 2);

// One rewrite flush on the first request after a build: Yoast's category-base stripping only registers its rules
// on a normal page load, so a flush inside the build itself leaves /<category>/ URLs as 404.
add_action('init', function () {
    if (get_option('zs_flush_rewrites')) { delete_option('zs_flush_rewrites'); flush_rewrite_rules(false); }
}, 99);

// Category archives live under the blog: /<blog>/<category>/ (Zap: no "category"/"נושא" base, Hebrew slugs).
// WordPress already links them there (the post permalink's front); Yoast's base-stripping writes the rules at the
// root, so they are moved under the blog base to match the links.
add_filter('category_rewrite_rules', function ($rules) {
    $blog = (int) get_option('page_for_posts');
    if (!$blog || !preg_match('#^/[^/%]+/%postname%/$#u', (string) get_option('permalink_structure'))) return $rules;
    // the request can arrive decoded or percent-encoded in either case, so the prefix matches all three
    $enc  = strtolower(get_post_field('post_name', $blog));
    $base = '(?:' . preg_quote(urldecode($enc), '#') . '|' . $enc . '|' . strtoupper($enc) . ')';
    $out = [];
    foreach ($rules as $k => $v) {
        // the slug group too: decoded (servers that hand WordPress a decoded path) or encoded in either case
        $k = preg_replace_callback('#\((%[0-9a-fA-F%-]+)\)#', function ($m) {
            $l = strtolower($m[1]);
            return '(' . preg_quote(urldecode($l), '#') . '|' . $l . '|' . strtoupper($l) . ')';
        }, $k);
        $out[$base . '/' . $k] = $v;
    }
    return $out;
}, 99);
// Hebrew slugs are stored percent-encoded in lower case; a request in upper case must still find the category.
add_filter('request', function ($qv) {
    if (!empty($qv['category_name']) && strpos($qv['category_name'], '%') !== false) $qv['category_name'] = strtolower($qv['category_name']);
    return $qv;
});
