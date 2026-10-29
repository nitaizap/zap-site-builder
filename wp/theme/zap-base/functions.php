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

/* ---------- Hello Elementor parent ----------
   Zap's base installs run Hello Elementor; this theme is its child so the base stays intact and Elementor Pro
   Theme Builder locations keep working. Hello's own CSS and meta tags are switched off: Zap Base styles
   everything, and Yoast owns the description (a second one fails QA). */
add_filter('hello_elementor_enqueue_style', '__return_false');
add_filter('hello_elementor_enqueue_theme_style', '__return_false');
add_filter('hello_elementor_header_footer', '__return_false');
add_filter('hello_elementor_description_meta_tag', '__return_false');
add_filter('hello_elementor_content_width', fn() => 1200);

/* ---------- assets ---------- */

function zs_font_slug($family) {
    return strtolower(str_replace(' ', '-', trim($family)));
}

add_action('wp_enqueue_scripts', function () {
    $dir = get_stylesheet_directory();
    $uri = get_stylesheet_directory_uri();
    $fonts = array_unique(array_filter([zs_opt('design.fonts.heading', 'Rubik'), zs_opt('design.fonts.body', 'Assistant')]));
    foreach ($fonts as $f) {
        $s = zs_font_slug($f);
        if (file_exists("$dir/fonts/$s.css")) {
            wp_enqueue_style("zs-font-$s", "$uri/fonts/$s.css", [], ZS_THEME_VER);
        }
    }
    wp_enqueue_style('zs-main', "$uri/assets/main.css", [], ZS_THEME_VER . '-' . filemtime("$dir/assets/main.css"));
    wp_add_inline_style('zs-main', zs_tokens_css());
    wp_enqueue_style('zs-finish', "$uri/assets/finish.css", ['zs-main'], ZS_THEME_VER . '-' . filemtime("$dir/assets/finish.css"));
    wp_enqueue_style('zs-pool', "$uri/assets/pool.css", ['zs-finish'], ZS_THEME_VER . '-' . filemtime("$dir/assets/pool.css"));
    // Zap QA standards (spacing, minimum text size, tap targets, FAQ, forms): loaded last so every preset obeys them
    wp_enqueue_style('zs-standards', "$uri/assets/standards.css", ['zs-pool'], ZS_THEME_VER . '-' . filemtime("$dir/assets/standards.css"));
    wp_enqueue_script('zs-site', "$uri/assets/site.js", [], ZS_THEME_VER . '-' . filemtime("$dir/assets/site.js"), ['strategy' => 'defer', 'in_footer' => true]);
}, 20);

/** Preload the two font files that paint the first screen. */
add_action('wp_head', function () {
    $dir = get_stylesheet_directory();
    $uri = get_stylesheet_directory_uri();
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
    // Elementor Site Settings (kit) own the brand values: the build writes them there, and a person who changes a
    // global colour or font in Elementor changes the whole site. Kit variables live on body (.elementor-kit-N),
    // so the tokens are re-declared on body; :root keeps the plain values as the fallback. Gate previews
    // (?zs_dir=) show their own colours, so they skip this layer.
    if (empty($_GET['zs_dir'])) {
        $kit = ['primary' => 'primary', 'primary-ink' => 'zsprimaryink', 'accent' => 'accent', 'accent-ink' => 'zsaccentink',
                'ink' => 'secondary', 'text' => 'text', 'muted' => 'zsmuted', 'bg' => 'zsbg', 'surface' => 'zssurf',
                'line' => 'zsline', 'dark' => 'zsdark', 'dark-ink' => 'zsdarkink'];
        $css .= 'body{';
        foreach ($kit as $k => $id) {
            $v = $c[str_replace('-', '_', $k)] ?? $c[$k] ?? $map[$k];
            if (preg_match('/^#[0-9a-fA-F]{3,8}$/', $v)) $css .= "--c-$k:var(--e-global-color-$id,$v);";
        }
        $css .= "--f-head:var(--e-global-typography-primary-font-family,'$h'),system-ui,sans-serif;"
              . "--f-body:var(--e-global-typography-text-font-family,'$b'),system-ui,sans-serif;}";
    }
    // Per-site escape hatch for the rare client-specific tweak; the shared theme stays untouched.
    if (!empty($d['custom_css']) && is_string($d['custom_css'])) {
        $css .= "\n" . wp_strip_all_tags($d['custom_css']);
    }
    return $css;
}

function zs_lum($hex) {
    $h = ltrim((string) $hex, '#');
    if (strlen($h) === 3) $h = $h[0] . $h[0] . $h[1] . $h[1] . $h[2] . $h[2];
    if (!preg_match('/^[0-9a-f]{6}$/i', $h)) return null;
    $c = array_map(function ($i) use ($h) { $v = hexdec(substr($h, $i, 2)) / 255; return $v <= .03928 ? $v / 12.92 : pow(($v + .055) / 1.055, 2.4); }, [0, 2, 4]);
    return .2126 * $c[0] + .7152 * $c[1] + .0722 * $c[2];
}
function zs_contrast($a, $b) {
    $x = zs_lum($a); $y = zs_lum($b);
    if ($x === null || $y === null) return 21;
    return (max($x, $y) + .05) / (min($x, $y) + .05);
}

add_filter('body_class', function ($classes) {
    $d = zs_design();
    // A saturated accent on a saturated primary (red on blue) blends in: the theme then uses white for accent
    // details on primary/dark grounds (eyebrows, dots, icons, buttons). Measured, not guessed.
    $col = $d['colors'] ?? [];
    if (!empty($col['accent']) && (zs_contrast($col['accent'], $col['primary'] ?? '#000') < 3 || zs_contrast($col['accent'], $col['dark'] ?? '#000') < 3))
        $classes[] = 'zs-accent-low';
    $classes[] = 'zs-p-' . sanitize_html_class($d['preset'] ?? 'clean');
    if (!empty($d['tone'])) $classes[] = 'zs-tone-' . sanitize_html_class($d['tone']);   // tone: light = no dark grounds anywhere
    $classes[] = 'zs-h-' . sanitize_html_class($d['header'] ?? 'light');
    $classes[] = 'zs-hv-' . sanitize_html_class($d['hero'] ?? 'split');
    $classes[] = 'zs-m-' . sanitize_html_class($d['motion'] ?? 'subtle');
    if (!empty($d['motif'])) $classes[] = 'zs-motif-' . sanitize_html_class($d['motif']);
    // header phone icon on phones is the default (Zap QA); header.mobile_call: false hides it when the client asks for one call button only
    if (zs_opt('header.mobile_call', true) === false) $classes[] = 'zs-no-mcall';   // brand shape: gables
    if (($d['header'] ?? 'light') === 'dark' && zs_opt('logo_light_id')) $classes[] = 'zs-has-logo-light';
    if (zs_is_elementor()) $classes[] = 'zs-built';
    if (is_page() && get_post_meta(get_the_ID(), '_zap_page_type', true) === 'contact') $classes[] = 'zs-is-contact';
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

/** The phones' fixed action bar (footer.php): call + WhatsApp, then `header.mobile_bar` items in order.
    An item is "waze" / "email" / "instagram" / "facebook", or {label, href, icon} (booking, delivery, menu: Zap portfolio,
    restaurants put הזמנת שולחן / משלוח / ניווט there). Up to 5 cells; with 3+ the cells turn into icon-over-label tiles. */
function zs_mobile_bar_items() {
    $out = [];
    foreach ((array) zs_opt('header.mobile_bar', []) as $it) {
        $k = is_array($it) ? ($it['type'] ?? '') : (string) $it;
        if ($k === 'waze' && (zs_opt('business.address') || zs_opt('business.geo'))) $out[] = ['ניווט', zs_waze_href(), 'waze', true];
        elseif ($k === 'email' && ($m = zs_opt('business.email_public'))) $out[] = ['מייל', 'mailto:' . $m, 'mail', false];
        elseif (in_array($k, ['instagram', 'facebook'], true) && ($u = zs_opt('business.' . $k))) $out[] = [$k === 'instagram' ? 'אינסטגרם' : 'פייסבוק', $u, $k, true];
        elseif (is_array($it) && !empty($it['label']) && !empty($it['href'])) $out[] = [$it['label'], $it['href'], $it['icon'] ?? 'calendar', str_starts_with($it['href'], 'http')];
    }
    return array_slice($out, 0, 3);
}

/** Waze navigation to the business: by coordinates when known, else by the address (Zap checklist: the address is a Waze link). */
function zs_waze_href() {
    $g = (array) zs_opt('business.geo', []);
    if (!empty($g['lat']) && !empty($g['lng'])) return 'https://waze.com/ul?ll=' . rawurlencode($g['lat'] . ',' . $g['lng']) . '&navigate=yes';
    return 'https://waze.com/ul?q=' . rawurlencode((string) zs_opt('business.address', '')) . '&navigate=yes';
}

function zs_wa_href($e164, $text = '') {
    $n = preg_replace('/\D/', '', (string) $e164);
    return 'https://wa.me/' . $n . ($text !== '' ? '?text=' . rawurlencode($text) : '');
}

function zs_breadcrumbs() {
    // Zap QA: no visible breadcrumb line above the H1. Yoast still emits BreadcrumbList in the schema graph;
    // a site that wants the visible trail sets header.breadcrumbs: true.
    if (!zs_opt('header.breadcrumbs', false)) return;
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
        'facebook' => '<path d="M14 21v-7h3l.5-3.5H14V8.6c0-1 .4-1.6 1.7-1.6h1.9V3.9c-.4 0-1.6-.2-2.9-.2-2.7 0-4.2 1.6-4.2 4.4v2.4H7.5V14h3v7"/>',
        'instagram' => '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.2 6.8h.01"/>',
        'linkedin' => '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/><path d="M8 10.5V16M8 7.8v.01M11.5 16v-5.5M11.5 13c0-1.5 1-2.6 2.4-2.6s2.1 1 2.1 2.6V16"/>',
        'youtube' => '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.5v5l4.3-2.5z"/>',
        'calendar' => '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
        'bag' => '<path d="M5 8h14l-1 12.5H6z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
        'waze' => '<path d="M5 15.5a7.5 7.5 0 1 1 13.6 1.9c-.6 1-1.6 1.6-2.6 1.6H9.6"/><circle cx="8" cy="19" r="1.6"/><circle cx="15" cy="19" r="1.6"/><path d="M10 10.5v.01M14.5 10.5v.01M10 13.5c1 .9 3.3.9 4.5 0"/>',
        'tiktok' => '<path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 2.5 2.3 4 4.5 4"/>',
    ];
    return '<svg class="zs-ico" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . ($p[$name] ?? '') . '</svg>';
}


/* ---------- site parts: shared by the Elementor header/footer templates (as shortcodes) and the PHP fallback ---------- */

/* "מספר מקשר": when the displayed phone is a Zap virtual number (business.phone_is_virtual), a small link next to it
   opens Zap's standard explanation (the wording of Zap's sites), with the business's regular number (business.phone_regular). */
function zs_vnote_btn() {
    if (!zs_opt('business.phone_is_virtual')) return '';
    return ' <button type="button" class="zs-vnote-btn" data-zs-vnote aria-haspopup="dialog">מספר מקשר</button>';
}
function zs_vnote_dialog() {
    if (!zs_opt('business.phone_is_virtual')) return '';
    $reg = trim((string) zs_opt('business.phone_regular', ''));
    return '<dialog class="zs-vnote" id="zs-vnote" aria-labelledby="zs-vnote-t"><p class="zs-vnote__t" id="zs-vnote-t">מספר מקשר</p>'
         . '<p>מספר זה הינו מספר וירטואלי, שהוא חלק משירות תוכן המופעל על ידי זאפ גרופ בע"מ ומפנה את המתקשר לבית העסק.</p>'
         . '<p>משתמש העושה שימוש במספר הווירטואלי, מסכים כי החברה תהא רשאית לשמור את מספר הטלפון ממנו התקשר, לכלול אותו במאגר מידע או ליצור באמצעותו קשר עם המשתמש, וכן כי המספר עשוי להשתנות מעת לעת.</p>'
         . ($reg ? '<p>מספר הטלפון הרגיל של בית העסק הוא <a href="' . esc_attr(zs_tel_href($reg)) . '" dir="ltr">' . esc_html($reg) . '</a>.</p>' : '')
         . '<form method="dialog"><button class="zs-vnote__x" aria-label="סגירה">×</button></form></dialog>';
}
add_action('wp_footer', function () { echo zs_vnote_dialog(); }, 5);

function zs_part_topbar_meta() {
    $tel = zs_opt('business.phone_e164'); $email = zs_opt('business.email_public'); $hours = (array) zs_opt('business.hours', []);
    $o = '<ul class="zs-topbar__list">';
    if ($hours) $o .= '<li>' . esc_html($hours[0]) . '</li>';
    if ($email) $o .= '<li><a href="mailto:' . esc_attr($email) . '">' . esc_html($email) . '</a></li>';
    // no phone here: the header's call button already shows it (Zap QA: one phone per header)
    return $o . '</ul>';
}

function zs_part_nav() {
    $tel = zs_opt('business.phone_e164'); $cta = zs_opt('header.cta_label', '');
    $o = '<nav id="zs-nav" class="zs-nav" aria-label="תפריט ראשי">';
    $o .= wp_nav_menu(['theme_location' => 'primary', 'container' => false, 'menu_class' => 'zs-menu', 'depth' => 2, 'fallback_cb' => false, 'echo' => false]) ?: '';
    if ($tel) $o .= '<a class="zs-btn zs-btn--primary zs-nav__cta" href="' . esc_attr(zs_tel_href($tel)) . '">' . zs_icon('phone') . '<span>' . esc_html($cta ?: zs_opt('business.phone_display')) . '</span></a>';
    $o .= '</nav><button class="zs-burger" type="button" aria-expanded="false" aria-controls="zs-nav" aria-label="פתיחת תפריט"><span></span><span></span><span></span></button>';
    return $o;
}

function zs_part_menu($location) {
    return wp_nav_menu(['theme_location' => $location, 'container' => false, 'menu_class' => 'zs-footer__links', 'depth' => 1, 'fallback_cb' => false, 'echo' => false]) ?: '';
}

function zs_part_footer_contact() {
    $tel = zs_opt('business.phone_e164'); $wa = zs_opt('business.whatsapp_e164');
    $wa_text = zs_opt('business.whatsapp_text', 'שלום, הגעתי מהאתר ואשמח לפרטים');
    $o = '<ul class="zs-footer__contact">';
    if ($tel) $o .= '<li>' . zs_icon('phone') . '<a href="' . esc_attr(zs_tel_href($tel)) . '">' . esc_html(zs_opt('business.phone_display')) . '</a>' . zs_vnote_btn() . '</li>';
    if ($wa)  $o .= '<li>' . zs_icon('whatsapp') . '<a href="' . esc_url(zs_wa_href($wa, $wa_text)) . '" target="_blank" rel="noopener">שלחו הודעת וואטסאפ</a></li>';
    if ($a = zs_opt('business.address')) $o .= '<li>' . zs_icon('pin') . '<a href="' . esc_url(zs_waze_href()) . '" target="_blank" rel="noopener">' . esc_html($a) . '<span class="zs-sr"> (ניווט בוויז, נפתח בחלון חדש)</span></a></li>';
    foreach ((array) zs_opt('business.hours', []) as $h) $o .= '<li>' . zs_icon('clock') . '<span>' . esc_html($h) . '</span></li>';
    return $o . zs_social_rows() . '</ul>';
}

/** Social profiles as rows of a contact list: the same icon size and alignment as phone/address, with a label. */
function zs_social_rows() {
    $nets = ['facebook' => 'ביקרו בפייסבוק שלנו', 'instagram' => 'עקבו אחרינו באינסטגרם', 'linkedin' => 'בקרו בלינקדאין שלנו',
             'youtube' => 'צפו בערוץ היוטיוב שלנו', 'tiktok' => 'עקבו אחרינו בטיקטוק'];
    $o = '';
    foreach ($nets as $k => $label) {
        $u = trim((string) zs_opt('business.' . $k, ''));
        if ($u === '' || !preg_match('#^https?://#i', $u)) continue;
        $o .= '<li class="zs-social-row zs-social-row--' . $k . '">' . zs_social_icon($k) . '<a href="' . esc_url($u)
            . '" target="_blank" rel="noopener">' . esc_html($label) . '<span class="zs-sr"> (נפתח בחלון חדש)</span></a></li>';
    }
    return $o;
}

/** Solid brand marks (recognisable at 20 px; the outline set is for UI icons). */
function zs_social_icon($k) {
    $p = [
        'facebook'  => '<path d="M13.6 21.5v-8h2.7l.4-3.2h-3.1V8.3c0-.9.3-1.6 1.6-1.6h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.3H7.4v3.2h2.8v8z"/>',
        'instagram' => '<path d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-8.9a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM12 4.6c2.4 0 2.7 0 3.6.1 2.4.1 3.6 1.3 3.7 3.7v7.2c-.1 2.4-1.2 3.6-3.7 3.7H8.4c-2.4-.1-3.6-1.3-3.7-3.7V8.4C4.8 6 5.9 4.8 8.4 4.7h3.6zM12 3c-2.4 0-2.8 0-3.7.1C5 3.2 3.2 5 3.1 8.3 3 9.2 3 9.6 3 12s0 2.8.1 3.7c.1 3.3 1.9 5.1 5.2 5.2H15.7c3.3-.1 5.1-1.9 5.2-5.2.1-.9.1-1.3.1-3.7s0-2.8-.1-3.7C20.8 5 19 3.2 15.7 3.1 14.8 3 14.4 3 12 3z"/>',
        'linkedin'  => '<path d="M6.9 8.6H3.6V20h3.3zM5.2 3.5a1.9 1.9 0 1 0 0 3.8 1.9 1.9 0 0 0 0-3.8zM20.4 13.6c0-3.1-1.7-5.2-4.4-5.2-1.5 0-2.5.8-3 1.6V8.6H9.8V20h3.3v-5.9c0-1.6.6-2.8 2.1-2.8s2 1.2 2 2.8V20h3.3z"/>',
        'youtube'   => '<path d="M21.6 7.2a2.6 2.6 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.6 2.6 0 0 0 2.4 7.2 27 27 0 0 0 2 12a27 27 0 0 0 .4 4.8 2.6 2.6 0 0 0 1.8 1.8c1.6.4 7.8.4 7.8.4s6.2 0 7.8-.4a2.6 2.6 0 0 0 1.8-1.8A27 27 0 0 0 22 12a27 27 0 0 0-.4-4.8zM10 15V9l5.2 3z"/>',
        'tiktok'    => '<path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-1.8-2.5V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.3 7.3 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/>',
    ];
    return '<svg class="zs-ico zs-ico--solid" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" stroke="none" aria-hidden="true" focusable="false">' . ($p[$k] ?? '') . '</svg>';
}

/** The business's social profiles (business.facebook / instagram / linkedin / youtube / tiktok) as icon links. */
function zs_part_social() {
    $nets = ['facebook' => 'פייסבוק', 'instagram' => 'אינסטגרם', 'linkedin' => 'לינקדאין', 'youtube' => 'יוטיוב', 'tiktok' => 'טיקטוק'];
    $o = '';
    foreach ($nets as $k => $label) {
        $u = trim((string) zs_opt('business.' . $k, ''));
        if ($u === '' || !preg_match('#^https?://#i', $u)) continue;
        $o .= '<li><a class="zs-social__' . $k . '" href="' . esc_url($u) . '" target="_blank" rel="noopener" aria-label="'
            . esc_attr($label . ' (נפתח בחלון חדש)') . '">' . zs_social_icon($k) . '</a></li>';
    }
    return $o ? '<ul class="zs-social">' . $o . '</ul>' : '';
}

function zs_part_copyright() {
    $name = zs_opt('business.name', get_bloginfo('name'));
    $note = zs_opt('footer.ai_images_note');
    return '<p class="zs-footer__copy">© ' . esc_html(date('Y') . ' ' . $name) . '. כל הזכויות שמורות' . ($note ? ' · ' . esc_html($note) : '') . '</p>';
}

function zs_part_legal() {
    $privacy = zs_opt('standards.privacy_url', home_url('/מדיניות-פרטיות/'));
    $a11y = zs_opt('standards.accessibility_url', home_url('/הצהרת-נגישות/'));
    // both legal links behave the same way: a new tab, so the visitor keeps their place (Zap QA)
    $nt = ' target="_blank" rel="noopener"';
    return '<ul class="zs-footer__legal"><li><a href="' . esc_url($privacy) . '"' . $nt . '>מדיניות פרטיות<span class="zs-sr"> (נפתח בחלון חדש)</span></a></li>'
         . '<li><a href="' . esc_url($a11y) . '"' . $nt . '>הצהרת נגישות<span class="zs-sr"> (נפתח בחלון חדש)</span></a></li></ul>';
}

function zs_part_group_logo() {
    // light footers carry Zap's colour logo (blue mark, navy word); dark footers the white credit image
    if ((zs_design()['tone'] ?? '') === 'light') {
        return '<a class="zs-footer__zap zs-footer__zap--color" href="https://zapgroup.co.il/" target="_blank" rel="noopener">'
             . '<span class="zs-footer__zap-by">Powered by</span><img src="' . esc_url(get_stylesheet_directory_uri() . '/assets/zap-group-blue.svg')
             . '" width="109" height="26" alt="זאפ גרופ" loading="lazy" decoding="async"></a>';
    }
    return '<a class="zs-footer__zap" href="https://zapgroup.co.il/" target="_blank" rel="noopener"><img src="'
         . esc_url(get_stylesheet_directory_uri() . '/assets/zap-group.webp') . '" width="183" height="26" alt="זאפ גרופ" loading="lazy" decoding="async"></a>';
}

function zs_part_call_line() {
    $tel = zs_opt('business.phone_e164');
    return $tel ? '<p class="zs-leadband__or">או התקשרו: <a href="' . esc_attr(zs_tel_href($tel)) . '">' . esc_html(zs_opt('business.phone_display')) . '</a></p>' : '';
}

foreach (['topbar_meta', 'nav', 'footer_contact', 'social', 'copyright', 'legal', 'group_logo', 'call_line'] as $zs_part) {
    add_shortcode("zap_$zs_part", fn() => call_user_func("zs_part_$zs_part"));
}
add_shortcode('zap_menu', fn($a) => zs_part_menu(shortcode_atts(['location' => 'footer'], $a)['location']));

/** Print the Elementor header/footer template for this slot. Elementor Pro Theme Builder first, then our saved template. */
function zs_render_tpl($slot) {
    if (function_exists('elementor_theme_do_location') && elementor_theme_do_location($slot)) return true;
    $id = (int) get_option("zs_tpl_$slot");
    if (!$id || !class_exists('\Elementor\Plugin') || get_post_status($id) !== 'publish') return false;
    $html = \Elementor\Plugin::instance()->frontend->get_builder_content_for_display($id, true);
    if (!$html) return false;
    echo '<div class="zs-tpl zs-tpl-' . esc_attr($slot) . '">' . $html . '</div>';
    return true;
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

/* ---------- scroll progress with a vehicle (design.progress: "scooter" | "van" | "truck") ----------
   A thin brand bar at the top of the viewport; the vehicle rides its tip while the page scrolls (site.js).
   Decorative only; the SVG comes from assets/vehicles, the same files the engine's road/route sections use. */
add_action('wp_footer', function () {
    $kind = sanitize_key((string) zs_opt('design.progress', ''));
    if (!$kind || is_admin()) return;
    $f = get_stylesheet_directory() . '/assets/vehicles/' . $kind . '.svg';
    if (!is_readable($f)) return;
    echo '<div class="zs-progress" aria-hidden="true"><span class="zs-progress__bar"></span><span class="zs-progress__v">'
        . preg_replace('/>\s+</', '><', trim((string) file_get_contents($f))) . '</span></div>';
}, 5);
