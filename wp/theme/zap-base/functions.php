<?php
/**
 * Zap Base theme. Everything visual reads design tokens from the `zap_site` option
 * written by the build engine, so one theme serves every client.
 */
defined('ABSPATH') || exit;

const ZS_THEME_VER = '1.0.0';

/** Read a dotted key from the zap_site option: zs_opt('business.phone_display'). */
function zs_opt($key = null, $default = '') {
    static $o = null;
    if ($o === null) {
        $o = get_option('zap_site', []);
    }
    if ($key === null) {
        return $o;
    }
    $v = $o;
    foreach (explode('.', $key) as $k) {
        if (!is_array($v) || !array_key_exists($k, $v)) {
            return $default;
        }
        $v = $v[$k];
    }
    return $v === null || $v === '' ? $default : $v;
}

add_action('after_setup_theme', function () {
    load_theme_textdomain('zap-base');
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo', ['flex-width' => true, 'flex-height' => true]);
    add_theme_support('html5', ['search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets']);
    add_theme_support('responsive-embeds');
    register_nav_menus([
        'primary' => 'תפריט ראשי',
        'footer'  => 'תפריט פוטר',
    ]);
    add_image_size('zs-card', 800, 560, true);
    add_image_size('zs-wide', 1600, 900, false);
});

/**
 * Hebrew sites are RTL even when no current he_IL core pack exists (WordPress reads the
 * direction from the core translation, and he_IL core packs stopped at 6.2).
 */
add_action('init', function () {
    if (str_starts_with(get_locale(), 'he') || zs_opt('site.dir') === 'rtl') {
        $GLOBALS['wp_locale']->text_direction = 'rtl';
    }
}, 0);
add_action('admin_init', function () {
    if (str_starts_with(get_user_locale(), 'he')) {
        $GLOBALS['wp_locale']->text_direction = 'rtl';
    }
}, 0);

/** Elementor needs to know the content width for boxed containers. */
add_action('after_setup_theme', function () {
    $GLOBALS['content_width'] = 1200;
}, 0);

/* ---------- assets ---------- */

function zs_font_slug($family) {
    return strtolower(str_replace(' ', '-', trim($family)));
}

add_action('wp_enqueue_scripts', function () {
    $dir = get_template_directory();
    $uri = get_template_directory_uri();
    $fonts = array_unique(array_filter([zs_opt('design.fonts.heading', 'Rubik'), zs_opt('design.fonts.body', 'Assistant')]));
    foreach ($fonts as $f) {
        $s = zs_font_slug($f);
        if (file_exists("$dir/fonts/$s.css")) {
            wp_enqueue_style("zs-font-$s", "$uri/fonts/$s.css", [], ZS_THEME_VER);
        }
    }
    wp_enqueue_style('zs-main', "$uri/assets/main.css", [], ZS_THEME_VER . '-' . filemtime("$dir/assets/main.css"));
    wp_add_inline_style('zs-main', zs_tokens_css());
    wp_enqueue_script('zs-site', "$uri/assets/site.js", [], ZS_THEME_VER . '-' . filemtime("$dir/assets/site.js"), ['strategy' => 'defer', 'in_footer' => true]);
}, 20);

/** Preload the two font files that paint the first screen. */
add_action('wp_head', function () {
    $dir = get_template_directory();
    $uri = get_template_directory_uri();
    $done = [];
    foreach ([zs_opt('design.fonts.heading', 'Rubik'), zs_opt('design.fonts.body', 'Assistant')] as $f) {
        $s = zs_font_slug($f);
        foreach (glob("$dir/fonts/$s/$s-hebrew-*.woff2") ?: [] as $file) {
            if (str_contains($file, "-italic")) continue;
            $u = "$uri/fonts/$s/" . basename($file);
            if (isset($done[$u])) continue;
            $done[$u] = 1;
            printf('<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url($u));
            break;
        }
    }
}, 2);

/** Active design: the build engine may store alternative directions for the gate-1 preview. */
function zs_design() {
    $d = zs_opt('design', []);
    $dirs = zs_opt('directions', []);
    if (!empty($_GET['zs_dir']) && is_array($dirs) && wp_get_environment_type() !== 'production') {
        $k = sanitize_key($_GET['zs_dir']);
        if (isset($dirs[$k]) && is_array($dirs[$k])) {
            $d = array_replace_recursive($d, $dirs[$k]);
        }
    }
    return $d;
}

function zs_tokens_css() {
    $d = zs_design();
    $c = $d['colors'] ?? [];
    $map = [
        'primary' => '#1d4ed8', 'primary-ink' => '#ffffff', 'accent' => '#f59e0b', 'accent-ink' => '#111827',
        'ink' => '#0f172a', 'text' => '#334155', 'muted' => '#64748b', 'bg' => '#ffffff',
        'surface' => '#f4f6fa', 'line' => '#e2e8f0', 'dark' => '#0b1220', 'dark-ink' => '#e8edf6',
    ];
    $css = ':root{';
    foreach ($map as $k => $def) {
        $key = str_replace('-', '_', $k);
        $v = $c[$key] ?? $c[$k] ?? $def;
        if (preg_match('/^#[0-9a-fA-F]{3,8}$/', $v)) {
            $css .= "--c-$k:$v;";
        }
    }
    $h = esc_attr($d['fonts']['heading'] ?? 'Rubik');
    $b = esc_attr($d['fonts']['body'] ?? 'Assistant');
    $css .= "--f-head:'$h',system-ui,sans-serif;--f-body:'$b',system-ui,sans-serif;";
    $r = (int) ($d['radius'] ?? 14);
    $css .= "--r:{$r}px;--r-sm:" . max(0, round($r * .6)) . 'px;--r-lg:' . round($r * 1.6) . 'px;';
    $css .= '}';
    // Per-site escape hatch for the rare client-specific tweak; the shared theme stays untouched.
    if (!empty($d['custom_css']) && is_string($d['custom_css'])) {
        $css .= "\n" . wp_strip_all_tags($d['custom_css']);
    }
    return $css;
}

add_filter('body_class', function ($classes) {
    $d = zs_design();
    $classes[] = 'zs-p-' . sanitize_html_class($d['preset'] ?? 'clean');
    $classes[] = 'zs-h-' . sanitize_html_class($d['header'] ?? 'light');
    $classes[] = 'zs-hv-' . sanitize_html_class($d['hero'] ?? 'split');
    $classes[] = 'zs-m-' . sanitize_html_class($d['motion'] ?? 'subtle');
    if (($d['header'] ?? 'light') === 'dark' && zs_opt('logo_light_id')) $classes[] = 'zs-has-logo-light';
    if (zs_is_elementor()) $classes[] = 'zs-built';
    return $classes;
});

/* ---------- helpers used by templates ---------- */

function zs_is_elementor($id = null) {
    $id = $id ?: get_the_ID();
    return $id && is_singular() && get_post_meta($id, '_elementor_edit_mode', true) === 'builder';
}

function zs_tel_href($e164) {
    return 'tel:' . preg_replace('/[^0-9+]/', '', (string) $e164);
}

function zs_wa_href($e164, $text = '') {
    $n = preg_replace('/\D/', '', (string) $e164);
    return 'https://wa.me/' . $n . ($text !== '' ? '?text=' . rawurlencode($text) : '');
}

function zs_breadcrumbs() {
    if (function_exists('yoast_breadcrumb') && !is_front_page()) {
        yoast_breadcrumb('<nav class="zs-crumbs" aria-label="פירורי לחם">', '</nav>');
    }
}

function zs_icon($name) {
    $p = [
        'phone' => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
        'whatsapp' => '<path d="M3 21l1.7-4.3A9 9 0 1 1 8 20z"/><path d="M8.6 8.4l1.6-.4 1 2-1 1c.6 1.3 1.6 2.3 2.9 2.9l1-1 2 1-.4 1.6c-3.7.2-7.3-3.4-7.1-7.1z"/>',
        'mail' => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'pin' => '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    ];
    return '<svg class="zs-ico" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . ($p[$name] ?? '') . '</svg>';
}

/* ---------- head hygiene ---------- */
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('wp_head', 'wp_generator');
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
add_filter('the_generator', '__return_empty_string');

/** Block-library CSS is only needed where Gutenberg content renders (posts). */
add_action('wp_enqueue_scripts', function () {
    if (zs_is_elementor()) {
        wp_dequeue_style('wp-block-library');
        wp_dequeue_style('wp-block-library-theme');
        wp_dequeue_style('global-styles');
        wp_dequeue_style('classic-theme-styles');
    }
}, 100);

add_filter('excerpt_length', fn() => 24);
add_filter('excerpt_more', fn() => '…');
