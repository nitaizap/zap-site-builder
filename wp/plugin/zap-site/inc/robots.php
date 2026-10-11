<?php
/**
 * A real robots.txt file, owned by the plugin.
 *
 * On nginx hosts (uPress and most managed hosts) /robots.txt is served only as a static file, so WordPress'
 * virtual robots.txt returns 404 there, and a hand-written file keeps the staging host after launch
 * (Yovel's trap #44). The plugin writes the file itself and rewrites it whenever the site address or the
 * indexing switch changes: deploy, domain switch, launch-day `blog_public = 1`. Same content on Apache.
 */
defined('ABSPATH') || exit;

function zap_robots_body() {
    if ((int) get_option('blog_public') !== 1) {   // int right after update_option, string when read from the DB
        return "User-agent: *\nDisallow: /\n";
    }
    return "User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php\n\nSitemap: " . home_url('/sitemap_index.xml') . "\n";
}

function zap_sync_robots($force = false) {
    $body = zap_robots_body();
    $sig  = md5($body);
    if (!$force && get_option('zap_robots_sig') === $sig) {
        return;
    }
    $file = ABSPATH . 'robots.txt';
    if (@file_put_contents($file, $body) !== false) {
        update_option('zap_robots_sig', $sig, false);
    }
}

add_action('init', 'zap_sync_robots', 20);
add_action('update_option_blog_public', fn() => zap_sync_robots(true));
add_action('update_option_home', fn() => zap_sync_robots(true));

/* Keep the virtual robots.txt identical, for hosts that do route it through WordPress. */
add_filter('robots_txt', fn() => zap_robots_body(), 99);
