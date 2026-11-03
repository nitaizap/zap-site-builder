<?php
/**
 * Launch-ready by itself: the site knows whether it runs on a staging address or on the client's domain, and
 * fixes everything that depends on it the first time it is opened on a new address. The launch manager migrates
 * the site (any tool: uPress clone, All-in-One, Duplicator, WPvivid...) and changes nothing.
 *
 *   staging address  → leads saved but not mailed to the client, noindex, robots.txt Disallow: /
 *   any other domain → leads mailed to the client, indexed, normal robots.txt + sitemap
 *
 * On a move (the stored address differs from the current one) it also rewrites the old address inside Elementor's
 * data (migration tools often skip Elementor's JSON, leaving images and links on the staging host), clears
 * Elementor's generated CSS and Yoast's cached URLs, and refreshes the permalinks. Decided by the address, never by
 * a flag in the database: a flag travels with the database and kept a live site silent (Zap QA, staging → live).
 */
defined('ABSPATH') || exit;

/** Zap's staging addresses (plus any host `zs push` registered in zap_staging_hosts). */
function zap_is_staging_host($host) {
    $host = strtolower((string) $host);
    if ($host === '' || in_array($host, ['localhost', '127.0.0.1'], true)) return true;
    foreach (['.ussl.co.il', '.zapsites.co.il', '.local', '.test'] as $suffix) {
        if (str_ends_with($host, $suffix)) return true;
    }
    return in_array($host, (array) get_option('zap_staging_hosts', []), true);
}

function zap_site_host() {
    return strtolower((string) parse_url(home_url(), PHP_URL_HOST));
}

/** True on a staging address (or a local/development WordPress). Everything staging-only asks this. */
function zap_is_staging() {
    if (in_array(wp_get_environment_type(), ['local', 'development'], true)) return true;
    return zap_is_staging_host(zap_site_host());
}

/* First request on a new address: switch the site to that address's mode and repair what a migration leaves behind. */
/** The site's origin without the scheme: host plus a non-default port ("example.co.il", "127.0.0.1:8740"). */
function zap_site_origin() {
    $u = parse_url(home_url());
    return strtolower(($u['host'] ?? '') . (isset($u['port']) ? ':' . $u['port'] : ''));
}

add_action('init', function () {
    $now = zap_site_origin();
    $was = (string) get_option('zap_site_host', '');
    if ($now === '' || $now === $was) return;
    update_option('zap_site_host', $now, true);

    $staging = zap_is_staging();
    update_option('blog_public', $staging ? '0' : '1');   // robots.txt follows (robots.php hooks this option)
    delete_option('zs_staging_lock');                      // the old database flag: obsolete, never trusted again

    if ($was !== '') {
        // Elementor stores absolute URLs (images, links) in its JSON; replace the old host on both schemes
        if (class_exists('\Elementor\Utils')) {
            // the full old origin (with its port), on both schemes, the escaped JSON form included
            foreach (['https://', 'http://'] as $from_s) {
                try { \Elementor\Utils::replace_urls($from_s . $was, home_url()); } catch (\Throwable $e) {}
            }
        }
        if (class_exists('\Elementor\Plugin') && isset(\Elementor\Plugin::$instance->files_manager)) {
            \Elementor\Plugin::$instance->files_manager->clear_cache();
        }
        // Yoast keeps each page's URL in its indexables table: empty it, Yoast rebuilds it with the new address
        global $wpdb;
        foreach (['yoast_indexable', 'yoast_indexable_hierarchy', 'yoast_seo_links'] as $t) {
            if ($wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $wpdb->prefix . $t))) $wpdb->query("TRUNCATE TABLE {$wpdb->prefix}$t");
        }
        flush_rewrite_rules(false);
    }
    do_action('zap_site_moved', $was, $now, $staging);
}, 1);

/* wp-admin: say which mode the site is in, so nobody has to guess (and nobody has to change anything). */
add_action('admin_notices', function () {
    if (!current_user_can('manage_options')) return;
    $s = get_current_screen();
    if (!$s || !in_array($s->id, ['dashboard', 'zap_lead_page_zap-form-settings'], true)) return;
    $msg = zap_is_staging()
        ? 'אתר סטייג\'ינג: פניות נשמרות ולא נשלחות ללקוח, והאתר חסום למנועי חיפוש. בכתובת הסופית של הלקוח הכול נפתח אוטומטית, בלי לשנות הגדרות.'
        : 'האתר באוויר: פניות נשלחות ל-' . esc_html(zap_opt('business.email_leads')) . ' והאתר פתוח למנועי חיפוש.';
    echo '<div class="notice notice-info"><p><strong>Zap Site:</strong> ' . $msg . '</p></div>';
});
