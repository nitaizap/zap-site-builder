<?php
/**
 * Build tasks executed inside WordPress (wp eval-file). Each zs_task_* takes the decoded JSON payload
 * written by build.py. Output: short one-line summaries; media prints a JSON map on its last line.
 */
defined('ABSPATH') || exit;

require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/post.php';
require_once ABSPATH . 'wp-admin/includes/nav-menu.php';

// Elementor's Document::save() silently refuses users who cannot edit; act as the site admin.
$zs_admin = get_users(['role' => 'administrator', 'number' => 1, 'orderby' => 'ID']);
if ($zs_admin) wp_set_current_user($zs_admin[0]->ID);
set_error_handler(fn($no, $str, $file) => str_contains((string) $file, 'wp_lib.php') ? false : true, E_WARNING | E_NOTICE | E_DEPRECATED | E_USER_DEPRECATED);

function zs_find($type, $key) {
    if ($key === '' || $key === null) $key = '__home';   // empty meta values never match reliably
    $q = get_posts(['post_type' => $type, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids',
                    'meta_key' => '_zs_key', 'meta_value' => $key, 'suppress_filters' => true]);
    return $q ? (int) $q[0] : 0;
}

/* ---------------- options ---------------- */
function zs_task_options($p) {
    update_option('zap_site', $p['zap_site']);
    update_option('blogname', $p['title']);
    update_option('blogdescription', $p['tagline'] ?? '');
    echo "options: saved\n";
}

/* ---------------- one zap_site key ---------------- */
function zs_task_set_option($p) {
    $o = get_option('zap_site', []);
    $o[$p['key']] = $p['value'];
    update_option('zap_site', $o);
}

/* ---------------- media ---------------- */
function zs_task_media($p) {
    $map = [];
    foreach ($p['items'] as $it) {
        $existing = get_posts(['post_type' => 'attachment', 'post_status' => 'inherit', 'numberposts' => 1, 'fields' => 'ids',
                               'meta_key' => '_zs_key', 'meta_value' => $it['key']]);
        $id = $existing ? (int) $existing[0] : 0;
        if ($id && get_post_meta($id, '_zs_hash', true) !== $it['hash']) {
            wp_delete_attachment($id, true);
            $id = 0;
        }
        if (!$id) {
            $tmp = wp_tempnam(basename($it['file']));
            copy($it['file'], $tmp);
            $file = ['name' => basename($it['file']), 'tmp_name' => $tmp];
            $id = media_handle_sideload($file, 0, $it['title'] ?: null);
            if (is_wp_error($id)) {
                @unlink($tmp);
                fwrite(STDERR, "media '{$it['key']}' failed: " . $id->get_error_message() . "\n");
                continue;
            }
            update_post_meta($id, '_zs_key', $it['key']);
            update_post_meta($id, '_zs_hash', $it['hash']);
        }
        update_post_meta($id, '_wp_attachment_image_alt', wp_slash($it['alt']));
        if (!empty($it['ai'])) {
            wp_update_post(['ID' => $id, 'post_content' => 'תמונה שנוצרה עבור האתר (AI) — אינה מתעדת את העסק בפועל.']);
        }
        $map[$it['key']] = ['id' => $id, 'url' => wp_get_attachment_url($id), 'alt' => $it['alt']];
    }
    echo wp_json_encode($map, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}

/* ---------------- pages ---------------- */
function zs_yoast_meta($seo, $noindex = false) {
    $m = [];
    if (!empty($seo['title']))       $m['_yoast_wpseo_title'] = $seo['title'];
    if (!empty($seo['description'])) $m['_yoast_wpseo_metadesc'] = $seo['description'];
    if (!empty($seo['keyword']))     $m['_yoast_wpseo_focuskw'] = $seo['keyword'];
    $m['_yoast_wpseo_meta-robots-noindex'] = $noindex ? '1' : '';
    return $m;
}

function zs_task_pages($p) {
    $ids = [];
    $made = $updated = 0;
    foreach ($p['pages'] as $pg) {
        $id = zs_find('page', $pg['key']);
        $parent = $pg['parent'] !== null ? ($ids[$pg['parent']] ?? zs_find('page', $pg['parent'])) : 0;
        $meta = array_merge([
            '_zs_key'         => $pg['key'] === '' ? '__home' : $pg['key'],
            '_zap_page_type'  => $pg['type'],
            '_zap_faq'        => $pg['faq'] ? wp_slash(wp_json_encode($pg['faq'], JSON_UNESCAPED_UNICODE)) : '',
            '_wp_page_template' => 'default',
        ], zs_yoast_meta($pg['seo'] ?? [], $pg['noindex']));
        $arr = [
            'post_type'    => 'page',
            'post_status'  => 'publish',
            'post_title'   => wp_slash($pg['title']),
            'post_name'    => $pg['slug'],
            'post_parent'  => $parent,
            'post_excerpt' => wp_slash($pg['excerpt']),
            'menu_order'   => (int) $pg['menu_order'],
            'post_content' => wp_slash($pg['content'] ?? ''),
            'meta_input'   => $meta,
            'comment_status' => 'closed',
        ];
        if ($id) { $arr['ID'] = $id; wp_update_post($arr); $updated++; }
        else     { $id = wp_insert_post($arr); $made++; }
        $ids[$pg['key']] = $id;

        if (!empty($pg['image'])) set_post_thumbnail($id, (int) $pg['image']);
        else delete_post_thumbnail($id);

        if (is_array($pg['elements'])) {
            $doc = \Elementor\Plugin::$instance->documents->get($id, false);
            $doc->set_is_built_with_elementor(true);
            $ok = $doc->save(['elements' => $pg['elements'], 'settings' => ['template' => 'default']]);
            if (!$ok) fwrite(STDERR, "elementor save refused for page '{$pg['key']}'\n");
        } else {
            delete_post_meta($id, '_elementor_edit_mode');
            delete_post_meta($id, '_elementor_data');
        }

        if ($pg['type'] === 'home') {
            update_option('show_on_front', 'page');
            update_option('page_on_front', $id);
        }
        if ($pg['type'] === 'blog') update_option('page_for_posts', $id);
        if ($pg['type'] === 'privacy') update_option('wp_page_for_privacy_policy', $id);
    }
    // Report pages that exist on the site but are no longer in site.json (never auto-deleted).
    $orphans = get_posts(['post_type' => 'page', 'post_status' => 'publish', 'numberposts' => -1, 'fields' => 'ids',
                          'post__not_in' => array_values($ids) ?: [0]]);
    echo "pages: $made created, $updated updated" . ($orphans ? ', orphans not in site.json: ' . implode(',', $orphans) : '') . "\n";
}

/* ---------------- posts ---------------- */
function zs_task_posts($p) {
    $cats = [];
    foreach ($p['categories'] as $c) {
        $t = get_term_by('slug', sanitize_title($c['slug']), 'category');
        $args = ['slug' => $c['slug'], 'description' => wp_slash($c['description'] ?? '')];
        if ($t) { wp_update_term($t->term_id, 'category', ['name' => wp_slash($c['name'])] + $args); $cats[$c['slug']] = $t->term_id; }
        else    { $r = wp_insert_term(wp_slash($c['name']), 'category', $args); if (!is_wp_error($r)) $cats[$c['slug']] = $r['term_id']; }
        if (!empty($c['seo'])) {
            $o = get_option('wpseo_taxonomy_meta', []);
            $o['category'][$cats[$c['slug']]] = ['wpseo_title' => $c['seo']['title'] ?? '', 'wpseo_desc' => $c['seo']['description'] ?? ''];
            update_option('wpseo_taxonomy_meta', $o);
        }
    }
    // 'Uncategorized' must not stay as an indexable archive.
    $unc = get_term_by('slug', 'uncategorized', 'category');
    if ($unc && $cats) { update_option('default_category', reset($cats)); wp_delete_term($unc->term_id, 'category'); }

    $n = 0;
    foreach ($p['posts'] as $po) {
        $id = zs_find('post', 'post:' . $po['slug']);
        $related = !empty($po['related']) ? zs_find('page', $po['related']) : 0;
        $arr = [
            'post_type'    => 'post',
            'post_status'  => 'publish',
            'post_title'   => wp_slash($po['title']),
            'post_name'    => $po['slug'],
            'post_excerpt' => wp_slash($po['excerpt'] ?? ''),
            'post_content' => wp_slash($po['html']),
            'post_category'=> array_values(array_filter([$cats[$po['category'] ?? ''] ?? 0])),
            'comment_status' => 'closed',
            'meta_input'   => array_merge([
                '_zs_key' => 'post:' . $po['slug'],
                '_zap_related_page' => $related,
                '_zap_faq' => !empty($po['faq']) ? wp_slash(wp_json_encode($po['faq'], JSON_UNESCAPED_UNICODE)) : '',
            ], zs_yoast_meta($po['seo'] ?? [])),
        ];
        if (!empty($po['date'])) { $arr['post_date'] = $po['date'] . ' 09:00:00'; }
        if ($id) { $arr['ID'] = $id; wp_update_post($arr); } else { $id = wp_insert_post($arr); }
        if (!empty($po['image'])) set_post_thumbnail($id, (int) $po['image']);
        $n++;
    }
    echo "posts: $n upserted, " . count($cats) . " categories\n";
}

/* ---------------- menus, SEO plugin, kit ---------------- */
function zs_menu($name, $location, $items) {
    $menu = wp_get_nav_menu_object($name);
    if ($menu) wp_delete_nav_menu($menu->term_id);
    $mid = wp_create_nav_menu($name);
    $add = function ($items, $parent) use (&$add, $mid) {
        $pos = 0;
        foreach ($items as $it) {
            $args = ['menu-item-title' => wp_slash($it['label']), 'menu-item-status' => 'publish',
                     'menu-item-parent-id' => $parent, 'menu-item-position' => ++$pos];
            $h = $it['href'] ?? '';
            if (str_starts_with($h, 'page:') && ($pid = zs_find('page', substr($h, 5))) ) {
                $args += ['menu-item-type' => 'post_type', 'menu-item-object' => 'page', 'menu-item-object-id' => $pid];
            } elseif (str_starts_with($h, 'category:') && ($t = get_term_by('slug', sanitize_title(substr($h, 9)), 'category'))) {
                $args += ['menu-item-type' => 'taxonomy', 'menu-item-object' => 'category', 'menu-item-object-id' => $t->term_id];
            } else {
                $args += ['menu-item-type' => 'custom', 'menu-item-url' => $h];
            }
            $iid = wp_update_nav_menu_item($mid, 0, $args);
            if (!empty($it['children'])) $add($it['children'], $iid);
        }
    };
    $add($items, 0);
    $loc = get_theme_mod('nav_menu_locations', []);
    $loc[$location] = $mid;
    set_theme_mod('nav_menu_locations', $loc);
}

function zs_task_finish($p) {
    if ($p['nav'])        zs_menu('ראשי', 'primary', $p['nav']);
    if ($p['footer_nav']) zs_menu('פוטר', 'footer', $p['footer_nav']);

    if (!empty($p['logo'])) {
        set_theme_mod('custom_logo', (int) $p['logo']);
        $meta = wp_get_attachment_metadata((int) $p['logo']);
        if ($meta && !empty($meta['width']) && abs($meta['width'] - $meta['height']) < 4 && $meta['width'] >= 512) {
            update_option('site_icon', (int) $p['logo']);
        }
    }
    update_option('blog_public', $p['blog_public'] ? '1' : '0');

    // Hebrew URLs only (Zap checklist: no /category/, no English bases):
    // posts at /<blog>/<post>/, categories at /<blog>/נושא/<category>/.
    $blog = (int) get_option('page_for_posts');
    if ($blog) {
        $base = urldecode(get_post_field('post_name', $blog));
        update_option('permalink_structure', '/' . $base . '/%postname%/');
        update_option('category_base', 'נושא');
        update_option('tag_base', 'תגית');
    } else {
        update_option('permalink_structure', '/%postname%/');
    }
    flush_rewrite_rules(true);

    // Yoast
    $b = $p['business'];
    $t = get_option('wpseo_titles', []);
    $t = array_merge($t, [
        'separator' => 'sc-pipe',
        'breadcrumbs-enable' => true,
        'breadcrumbs-home' => 'דף הבית',
        'breadcrumbs-sep' => '›',
        'company_or_person' => 'company',
        'company_name' => $b['name'],
        'company_logo' => !empty($p['logo']) ? wp_get_attachment_url((int) $p['logo']) : '',
        'company_logo_id' => (int) ($p['logo'] ?? 0),
        'disable-author' => true,
        'disable-date' => true,
        'disable-post_format' => true,
        'disable-attachment' => true,
        'noindex-tax-post_tag' => true,
        'title-404-wpseo' => 'העמוד לא נמצא %%sep%% %%sitename%%',
        'title-tax-category' => '%%term_title%% %%sep%% %%sitename%%',
        'metadesc-tax-category' => '%%category_description%%',
        'stripcategorybase' => false,
    ]);
    update_option('wpseo_titles', $t);
    $s = get_option('wpseo_social', []);
    if (!empty($p['og_image'])) {
        $s['og_default_image'] = wp_get_attachment_url((int) $p['og_image']);
        $s['og_default_image_id'] = (int) $p['og_image'];
    }
    $s['opengraph'] = true;
    foreach (['facebook' => 'facebook_site', 'instagram' => 'instagram_url', 'linkedin' => 'linkedin_url', 'youtube' => 'youtube_url'] as $k => $opt) {
        if (!empty($b[$k])) $s[$opt] = $b[$k];
    }
    update_option('wpseo_social', $s);
    $w = get_option('wpseo', []);
    $w['tracking'] = false;
    $w['show_onboarding_notice'] = false;
    $w['should_redirect_after_install_free'] = false;
    update_option('wpseo', $w);

    // Elementor kit: same palette + fonts in the editor UI, so editors pick brand values.
    $kit_id = (int) get_option('elementor_active_kit');
    if ($kit_id) {
        $c = $p['design']['colors'] ?? [];
        $f = $p['design']['fonts'] ?? [];
        $s = get_post_meta($kit_id, '_elementor_page_settings', true) ?: [];
        $s['system_colors'] = [
            ['_id' => 'primary',   'title' => 'ראשי',   'color' => $c['primary'] ?? '#1d4ed8'],
            ['_id' => 'secondary', 'title' => 'משני',   'color' => $c['ink'] ?? '#0f172a'],
            ['_id' => 'text',      'title' => 'טקסט',   'color' => $c['text'] ?? '#334155'],
            ['_id' => 'accent',    'title' => 'הדגשה', 'color' => $c['accent'] ?? '#f59e0b'],
        ];
        $s['custom_colors'] = [
            ['_id' => 'zsbg', 'title' => 'רקע', 'color' => $c['bg'] ?? '#ffffff'],
            ['_id' => 'zssurf', 'title' => 'משטח', 'color' => $c['surface'] ?? '#f4f6fa'],
            ['_id' => 'zsdark', 'title' => 'כהה', 'color' => $c['dark'] ?? '#0b1220'],
        ];
        $fam = fn($id, $title, $font, $w) => ['_id' => $id, 'title' => $title, 'typography_typography' => 'custom',
                                             'typography_font_family' => $font, 'typography_font_weight' => $w];
        $s['system_typography'] = [
            $fam('primary', 'כותרות', $f['heading'] ?? 'Rubik', '700'),
            $fam('secondary', 'כותרות משנה', $f['heading'] ?? 'Rubik', '600'),
            $fam('text', 'גוף', $f['body'] ?? 'Assistant', '400'),
            $fam('accent', 'כפתורים', $f['body'] ?? 'Assistant', '600'),
        ];
        $s['container_width'] = ['unit' => 'px', 'size' => 1200, 'sizes' => []];
        $s['space_between_widgets'] = ['column' => '0', 'row' => '0', 'isLinked' => true, 'unit' => 'px'];
        $s['site_name'] = $b['name'];
        if (!empty($p['logo'])) $s['site_logo'] = ['id' => (int) $p['logo'], 'url' => wp_get_attachment_url((int) $p['logo'])];
        update_post_meta($kit_id, '_elementor_page_settings', wp_slash($s));
    }
    echo "finish: menus, logo, yoast, kit\n";
}
