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
    // Elementor + site defaults the design relies on. Applied on every build (not only at create time) because a
    // pushed site starts from Zap's cloned base, where Elementor's default colours/fonts would repaint headings
    // and buttons.
    foreach ([
        'elementor_disable_color_schemes' => 'yes', 'elementor_disable_typography_schemes' => 'yes',
        'elementor_google_font' => '0', 'elementor_font_display' => 'swap', 'elementor_load_fa4_shim' => '',
        'elementor_unfiltered_files_upload' => '', 'elementor_onboarded' => '1', 'elementor_tracker_notice' => '1',
        'elementor_allow_tracking' => 'no', 'default_comment_status' => 'closed', 'default_ping_status' => 'closed',
        'timezone_string' => 'Asia/Jerusalem', 'date_format' => 'd/m/Y', 'wpseo_titles_sep' => 'sc-pipe',
    ] as $k => $v) update_option($k, $v);
    update_option('elementor_cpt_support', ['page', 'post']);
    if (get_option('permalink_structure') !== '/%postname%/') update_option('permalink_structure', '/%postname%/');
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
        // the media title is what Elementor's lightbox shows as the caption: the Hebrew description, never the file name
        if ($it['alt'] !== '' && get_the_title($id) !== $it['alt']) wp_update_post(['ID' => $id, 'post_title' => wp_slash($it['alt'])]);
        if (!empty($it['ai'])) {
            wp_update_post(['ID' => $id, 'post_content' => 'תמונה שנוצרה עבור האתר (AI) — אינה מתעדת את העסק בפועל.']);
        }
        $map[$it['key']] = ['id' => $id, 'url' => wp_get_attachment_url($id), 'alt' => $it['alt']];
    }
    echo wp_json_encode($map, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}

/* ---------------- what the server already holds (push skips unchanged media and pages) ---------------- */
function zs_task_state($p) {
    $out = ['media' => [], 'pages' => []];
    foreach (get_posts(['post_type' => 'attachment', 'post_status' => 'inherit', 'numberposts' => -1, 'meta_key' => '_zs_key']) as $a) {
        $out['media'][get_post_meta($a->ID, '_zs_key', true)] = ['hash' => get_post_meta($a->ID, '_zs_hash', true), 'id' => $a->ID,
            'url' => wp_get_attachment_url($a->ID)];
    }
    foreach (get_posts(['post_type' => ['page', 'post'], 'post_status' => 'any', 'numberposts' => -1, 'meta_key' => '_zs_key']) as $q) {
        $out['pages'][get_post_meta($q->ID, '_zs_key', true)] = get_post_status($q->ID) === 'publish' ? get_post_meta($q->ID, '_zs_phash', true) : '';
    }
    echo wp_json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
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
        if (!empty($pg['phash'])) update_post_meta($id, '_zs_phash', $pg['phash']);   // lets a later push skip it when unchanged

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
        if ($pg['type'] === 'privacy' && empty($pg['legal'])) update_option('wp_page_for_privacy_policy', $id);
    }
    // Report pages that exist on the site but are no longer in site.json (the engine's own pages are drafted below).
    $known = array_values($ids);
    foreach ($p['all_keys'] ?? [] as $k) { $kid = zs_find('page', $k); if ($kid) $known[] = $kid; }   // batched builds
    $orphans = get_posts(['post_type' => 'page', 'post_status' => 'publish', 'numberposts' => -1, 'fields' => 'ids',
                          'post__not_in' => $known ?: [0]]);
    // A page this engine built (it carries _zs_key) whose key left site.json (a renamed URL) goes to draft, so the
    // old URL never stays live beside the new one; pages the engine did not build are only reported.
    $drafted = [];
    foreach ($orphans as $oid) {
        if (get_post_meta($oid, '_zs_key', true) !== '') { wp_update_post(['ID' => $oid, 'post_status' => 'draft']); $drafted[] = $oid; }
    }
    $orphans = array_diff($orphans, $drafted);
    echo "pages: $made created, $updated updated" . ($orphans ? ', orphans not in site.json: ' . implode(',', $orphans) : '') . ($drafted ? ', renamed/removed pages drafted: ' . implode(',', $drafted) : '') . "\n";
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
    // Nor may a category left over from the cloned base site (a Latin slug, e.g. /blog/) that site.json does not own.
    if ($cats) {
        update_option('default_category', reset($cats));
        foreach (get_terms(['taxonomy' => 'category', 'hide_empty' => false]) as $t) {
            if (in_array($t->term_id, $cats, true)) continue;
            if ($t->slug === 'uncategorized' || preg_match('/^[a-z0-9-]+$/', urldecode($t->slug))) wp_delete_term($t->term_id, 'category');
        }
    }

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
    // Elementor's per-document HTML cache can outlive a rebuild (a fresh site served its header without the
    // menu and burger until it was cleared): drop it every build, Elementor regenerates it on the next view
    delete_post_meta_by_key('_elementor_element_cache');
    if ($p['nav'])        zs_menu('ראשי', 'primary', $p['nav']);
    if ($p['footer_nav']) zs_menu('פוטר', 'footer', $p['footer_nav']);

    if (!empty($p['logo'])) {
        set_theme_mod('custom_logo', (int) $p['logo']);
        $meta = wp_get_attachment_metadata((int) $p['logo']);
        if ($meta && !empty($meta['width']) && abs($meta['width'] - $meta['height']) < 4 && $meta['width'] >= 512) {
            update_option('site_icon', (int) $p['logo']);
        }
    }
    if (!empty($p['favicon'])) update_option('site_icon', (int) $p['favicon']);   // never keep the clone's icon
    update_option('blog_public', $p['blog_public'] ? '1' : '0');

    // Hebrew URLs only (Zap checklist: no /category/, no English bases):
    // posts at /<blog>/<post>/, categories at /<blog>/נושא/<category>/.
    $blog = (int) get_option('page_for_posts');
    if ($blog) {
        $base = urldecode(get_post_field('post_name', $blog));
        update_option('permalink_structure', '/' . $base . '/%postname%/');
        update_option('category_base', '');   // no base in category URLs (Zap checklist); Yoast strips it
        update_option('tag_base', 'תגית');
    } else {
        update_option('permalink_structure', '/%postname%/');
    }

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
        'title-404-wpseo' => '%%sitename%% %%sep%% העמוד לא נמצא',
        'title-tax-category' => '%%sitename%% %%sep%% %%term_title%%',   // Zap: "<client> | <page>"
        'title-post' => '%%sitename%% %%sep%% %%title%%',
        'title-page' => '%%sitename%% %%sep%% %%title%%',
        'metadesc-tax-category' => '%%category_description%%',
        'stripcategorybase' => true,
    ]);
    update_option('wpseo_titles', $t);
    flush_rewrite_rules(true);   // after Yoast: stripcategorybase adds its own rules
    update_option('zs_flush_rewrites', 1);   // and once more on the next request, when Yoast's rewrite filters are loaded
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
            ['_id' => 'zsdarkink', 'title' => 'טקסט על כהה', 'color' => $c['dark_ink'] ?? '#e8edf6'],
            ['_id' => 'zsprimaryink', 'title' => 'טקסט על ראשי', 'color' => $c['primary_ink'] ?? '#ffffff'],
            ['_id' => 'zsaccentink', 'title' => 'טקסט על הדגשה', 'color' => $c['accent_ink'] ?? '#111827'],
            ['_id' => 'zsmuted', 'title' => 'טקסט משני', 'color' => $c['muted'] ?? '#64748b'],
            ['_id' => 'zsline', 'title' => 'קווים', 'color' => $c['line'] ?? '#e2e8f0'],
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

/* ---------------- header / footer templates ----------------
   Saved as Elementor documents so a person edits them in Elementor like any page. With Elementor Pro they are
   Theme Builder 'header'/'footer' templates shown site-wide (include/general); without Pro they are plain
   saved templates that the Zap Base theme renders in the same places. Stable by _zs_key, rebuilt in place. */
function zs_task_templates($p) {
    $pro = defined('ELEMENTOR_PRO_VERSION');
    $out = [];
    // header/footer always; with Elementor Pro also the blog's Single post + Archive templates (Zap QA: system pages
    // are Theme Builder templates, editable in Elementor, not theme PHP). Without Pro the theme's PHP renders them.
    $slots = $pro ? ['header', 'footer', 'single-post', 'archive'] : ['header', 'footer'];
    $conds = ['header' => ['include/general'], 'footer' => ['include/general'],
              'single-post' => ['include/singular/post'], 'archive' => ['include/archive']];
    $titles = ['header' => 'Header', 'footer' => 'Footer', 'single-post' => 'פוסט בבלוג', 'archive' => 'בלוג וקטגוריות'];
    foreach ($slots as $slot) {
        if (empty($p[$slot])) continue;
        $type = $pro ? $slot : 'section';
        $id = zs_find('elementor_library', "__tpl_$slot");
        if ($id && get_post_meta($id, '_elementor_template_type', true) !== $type) { wp_delete_post($id, true); $id = 0; }
        if (!$id) {
            $doc = \Elementor\Plugin::$instance->documents->create($type, [
                'post_title' => $titles[$slot] . ': ' . $p['name'], 'post_status' => 'publish']);
            if (is_wp_error($doc) || !$doc) { fwrite(STDERR, "template create failed: $slot\n"); continue; }
            $id = $doc->get_main_id();
            update_post_meta($id, '_zs_key', "__tpl_$slot");
        }
        $doc = \Elementor\Plugin::$instance->documents->get($id, false);
        $doc->save(['elements' => $p[$slot]]);
        if ($pro) {
            update_post_meta($id, '_elementor_conditions', $conds[$slot]);
        }
        update_option("zs_tpl_$slot", $id);
        $out[] = "$slot=$id";
    }
    if ($pro && class_exists('\ElementorPro\Modules\ThemeBuilder\Module')) {
        try {   // refresh Pro's display-condition cache; an API change must never fail the whole build
            \ElementorPro\Modules\ThemeBuilder\Module::instance()->get_conditions_manager()->get_cache()->regenerate();
        } catch (\Throwable $e) {
            fwrite(STDERR, 'theme builder cache: ' . $e->getMessage() . "\n");
        }
    }
    echo 'templates: ' . implode(' ', $out) . ($pro ? ' (Theme Builder)' : ' (saved templates)') . "\n";
}
