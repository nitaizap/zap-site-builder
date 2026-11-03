<?php
/**
 * Safety net for a site that kept the theme but lost the plugin.
 *
 * Zap's behaviour lives in the `zap-site` plugin: every `zap-*` Elementor widget (menu, logo, lead form, legal line,
 * contact list) and inc/launch.php (staging vs live by address). The theme travels with a migrated site; the plugin
 * may not (uPress clone, All-in-One, Duplicator, WPvivid copy what they are pointed at). Elementor drops a widget
 * whose type is not registered without a word, so a site that lost the plugin keeps answering HTTP 200 while it has
 * no menu and no form. That is what went live on thewhite-villa.co.il.
 *
 * This file is a loud signal and a minimal lifeline, NOT a second implementation: behaviour belongs in a plugin, so
 * nothing of the plugin's is rebuilt here. When the plugin is not running it
 *   1. says so in wp-admin on every screen (and in the admin bar on the site), naming what breaks and how to fix it;
 *   2. renders a plain list of the site's own menu links when the header came out without any navigation;
 *   3. puts `zs-plugin-missing` on <body>, which `zs launch-check` reads from the public html.
 * When the plugin IS running, nothing below is hooked at all: no filter, no action, no CSS, no markup.
 *
 * (WordPress has no way for a theme to require a plugin: the "Requires Plugins" header exists for plugins only, and
 * TGMPA, the library themes use, is a heavy second installer. A notice plus a fallback is the idiomatic minimum.)
 */
defined('ABSPATH') || exit;

/** The plugin's main file defines this constant; plugins load before the theme, so it is settled when this runs. */
function zs_plugin_missing() {
    return !defined('ZAP_SITE_VER');
}

/** 'inactive' when the plugin folder is on the server but switched off, 'absent' when it is not there at all. */
function zs_plugin_state() {
    if (!function_exists('get_plugins')) require_once ABSPATH . 'wp-admin/includes/plugin.php';
    foreach (get_plugins() as $file => $data) {
        if (dirname($file) === 'zap-site' || ($data['Name'] ?? '') === 'Zap Site') return ['inactive', $file];
    }
    return ['absent', ''];
}

/** The links of the site's own menu, as a <ul>: the "primary" location, else the first menu there is, else the top pages. */
function zs_fallback_links($class = 'zs-fallback-nav__list') {
    $args = ['container' => false, 'menu_class' => $class, 'depth' => 1, 'fallback_cb' => false, 'echo' => false];
    $menu = '';
    if (has_nav_menu('primary')) {
        $menu = (string) wp_nav_menu($args + ['theme_location' => 'primary']);
    } elseif ($menus = wp_get_nav_menus()) {
        $menu = (string) wp_nav_menu($args + ['menu' => $menus[0]]);
    }
    if (trim(wp_strip_all_tags($menu)) !== '') return $menu;
    $pages = (string) wp_list_pages(['title_li' => '', 'depth' => 1, 'number' => 8, 'sort_column' => 'menu_order,post_title',
                                     'exclude' => (int) get_option('page_on_front'), 'echo' => false]);
    $home = '<li class="page_item"><a href="' . esc_url(home_url('/')) . '">דף הבית</a></li>';
    return '<ul class="' . esc_attr($class) . '">' . $home . $pages . '</ul>';
}

/** The emergency navigation: a plain <nav> of links, no script, wraps on a phone. Only ever called with the plugin missing. */
function zs_fallback_nav() {
    return '<nav class="zs-fallback-nav" aria-label="תפריט ראשי" data-zs-fallback="plugin-missing">' . zs_fallback_links() . '</nav>';
}

/** The header the Theme Builder printed has no navigation at all (no <nav>, no menu widget of any kind): add the lifeline. */
function zs_header_needs_fallback($html) {
    return !preg_match('/<nav[\s>]|zs-menu|zs-burger|elementor-nav-menu|e-n-menu|role=["\']navigation/i', (string) $html);
}

if (zs_plugin_missing()) {
    /* 1. the signal: wp-admin, every screen, for anyone who can fix it. is-dismissible hides it for the page only; it is
          back on the next load until the plugin runs. */
    $zs_notice = function () {
        if (!current_user_can('activate_plugins')) return;
        [$state, $file] = zs_plugin_state();
        $fix = $state === 'inactive'
            ? 'התוסף מותקן אבל כבוי: <a class="button button-primary" href="' . esc_url(wp_nonce_url(self_admin_url('plugins.php?action=activate&plugin=' . rawurlencode($file)), 'activate-plugin_' . $file)) . '">הפעילו את Zap Site עכשיו</a>'
            : 'התוסף לא קיים בשרת. התקינו את <code>zap-site</code> (התיקייה <code>wp/plugin/zap-site</code> במאגר האתרים של זאפ; <code>zs push --live</code> מתקין אותו יחד עם התבנית).';
        echo '<div class="notice notice-error is-dismissible zs-plugin-missing-notice" style="border-left-width:8px"><p><strong>חסר התוסף Zap Site (zap-site). האתר הזה עובד חצי.</strong></p>'
           . '<p>התבנית Zap Base הועברה אבל התוסף לא, ובלעדיו: <strong>אין תפריט ניווט ולוגו</strong> (מוצג רק תפריט חירום פשוט), <strong>אין טופס פניות</strong> (האתר לא יכול לקבל פנייה מלקוח), '
           . '<strong>נעלמו השורה המשפטית, פרטי הקשר והקרדיט בפוטר</strong>, ו<strong>ההשקה אינה אוטומטית</strong>: חסימת מנועי חיפוש בסטייג\'ינג, שליחת הפניות ללקוח ותיקון כתובות אחרי העברה לא פועלים.</p>'
           . '<p>' . $fix . '</p>'
           . '<p dir="ltr" style="opacity:.8">The <b>Zap Site</b> plugin is not running: the Zap widgets (menu, logo, lead form, legal line, contact list) render as nothing and launch behaviour is off. Install and activate <code>zap-site</code>.</p></div>';
    };
    add_action('admin_notices', $zs_notice);
    add_action('network_admin_notices', $zs_notice);

    // the same signal on the site itself, for the person who is logged in to look at it
    add_action('admin_bar_menu', function ($bar) {
        if (!current_user_can('activate_plugins')) return;
        $bar->add_node(['id' => 'zs-plugin-missing', 'title' => '⚠ חסר התוסף Zap Site: אין תפריט וטופס',
                        'href' => admin_url('plugins.php'), 'meta' => ['class' => 'zs-plugin-missing-bar', 'title' => 'התוסף zap-site לא פעיל']]);
    }, 100);
    add_action('wp_head', function () { if (is_admin_bar_showing()) echo '<style>#wp-admin-bar-zs-plugin-missing>.ab-item{background:#b32d2e!important;color:#fff!important;font-weight:600}</style>' . "\n"; }, 99);

    /* 2. the lifeline's look: the theme's tokens, nothing else (loaded only here, after the theme's own stylesheet) */
    add_action('wp_enqueue_scripts', function () {
        wp_add_inline_style('zs-main',
            '.zs-fallback-nav{background:var(--c-surface,#f4f6fa);border-bottom:1px solid var(--c-line,#e2e8f0);padding:.5rem 1rem}'
          . '.zs-fallback-nav ul{display:flex;flex-wrap:wrap;gap:0 1.25rem;justify-content:center;margin:0;padding:0;list-style:none}'
          . '.zs-fallback-nav a{display:inline-block;padding:.7rem .25rem;color:var(--c-ink,#0f172a);font:600 1rem/1.4 var(--f-body,system-ui,sans-serif);text-decoration:none}'
          . '.zs-fallback-nav a:hover,.zs-fallback-nav a:focus-visible{text-decoration:underline}');
    }, 21);

    // 3. what `zs launch-check` reads
    add_filter('body_class', function ($classes) { $classes[] = 'zs-plugin-missing'; return $classes; });
}
