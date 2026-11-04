<?php
/**
 * Native Elementor widgets for the dynamic and shared site parts (form, menus, posts, map, contact details,
 * footer credits, blog templates). New sites place these widgets in the Elementor data; no shortcode text is
 * stored anywhere in the page content. Each widget renders through the same PHP as the legacy [zap_*]
 * shortcodes, which stay registered only so sites built before this change keep working.
 */
defined('ABSPATH') || exit;

add_action('elementor/elements/categories_registered', function ($m) {
    $m->add_category('zap', ['title' => 'Zap', 'icon' => 'eicon-site-identity']);
});

add_action('elementor/widgets/register', function ($wm) {
    if (!class_exists('\Elementor\Widget_Base')) return;

    abstract class Zap_Part_Widget extends \Elementor\Widget_Base {
        /** [widget name suffix, part tag, Hebrew title, eicon, controls: key => [type, label, default]] */
        abstract protected static function spec(): array;
        public function get_name() { return 'zap-' . static::spec()[0]; }
        public function get_title() { return static::spec()[2]; }
        public function get_icon() { return static::spec()[3]; }
        public function get_categories() { return ['zap']; }
        public function get_keywords() { return ['zap', static::spec()[0]]; }
        protected function is_dynamic_content(): bool { return true; }
        protected function register_controls() {
            $controls = static::spec()[4] ?? [];
            $this->start_controls_section('zs_content', ['label' => static::spec()[2]]);
            if (!$controls) {
                $this->add_control('zs_note', ['type' => \Elementor\Controls_Manager::RAW_HTML,
                    'raw' => 'התוכן נלקח אוטומטית מהגדרות האתר (פרטי העסק, תפריטים, פוסטים).']);
            }
            if (static::spec()[0] === 'form') {   // where the leads go, visible right in the editor (Zap QA)
                $to = function_exists('zap_opt') ? zap_opt('business.email_leads') : '';
                $this->add_control('zs_mail_note', ['type' => \Elementor\Controls_Manager::RAW_HTML,
                    'raw' => 'פניות נשלחות אל: <strong dir="ltr">' . esc_html($to ?: 'לא הוגדר') . '</strong><br>שולח: <span dir="ltr">' . esc_html(function_exists('zap_mail_from_address') ? zap_mail_from_address() : 'zapsites@d.co.il') . '</span><br>לשינוי: פניות מהאתר ← הגדרות טפסים.']);
            }
            foreach ($controls as $key => [$type, $label, $default]) {
                $c = ['label' => $label, 'default' => $default];
                if ($type === 'switch') {
                    $c += ['type' => \Elementor\Controls_Manager::SWITCHER, 'return_value' => 'yes'];
                } elseif ($type === 'number') {
                    $c += ['type' => \Elementor\Controls_Manager::NUMBER, 'min' => 1, 'max' => 12];
                } elseif (is_array($type)) {
                    $c += ['type' => \Elementor\Controls_Manager::SELECT, 'options' => $type];
                } else {
                    $c += ['type' => \Elementor\Controls_Manager::TEXT];
                }
                $this->add_control($key, $c);
            }
            $this->end_controls_section();
        }
        protected function render() {
            $tag = 'zap_' . static::spec()[1];
            $cb = $GLOBALS['shortcode_tags'][$tag] ?? null;
            if (!is_callable($cb)) return;
            $atts = [];
            foreach (array_keys(static::spec()[4] ?? []) as $key) {
                $v = $this->get_settings_for_display($key);
                $atts[$key] = static::spec()[4][$key][0] === 'switch' ? ($v === 'yes' ? 'yes' : 'no') : (string) $v;
            }
            $out = (string) call_user_func($cb, $atts, '', $tag);
            if ($out !== '') echo '<div class="zs-part zs-part--' . esc_attr(static::spec()[0]) . '">' . $out . '</div>';
        }
    }

    $yn = 'switch';
    $specs = [
        'form'           => ['form', 'form', 'טופס לידים', 'eicon-form-horizontal', [
            'id' => ['text', 'מזהה טופס', 'main'], 'message' => [$yn, 'שדה הודעה', 'yes'],
            'email' => [$yn, 'שדה אימייל', ''], 'button' => ['text', 'טקסט כפתור', '']]],
        'recent-posts'   => ['recent-posts', 'recent_posts', 'פוסטים אחרונים', 'eicon-posts-grid', [
            'count' => ['number', 'מספר פוסטים', 3], 'category' => ['text', 'קטגוריה (slug)', ''], 'exclude' => ['text', 'להחריג (ID)', '']]],
        'logo'           => ['logo', 'logo', 'לוגו האתר', 'eicon-site-logo', ['where' => [['header' => 'הדר', 'footer' => 'פוטר', 'footer-dark' => 'פוטר כהה (לוגו בהיר)'], 'מיקום', 'header']]],
        'nap'            => ['nap', 'nap', 'פרטי העסק', 'eicon-info-box', []],
        'map'            => ['map', 'map', 'מפה', 'eicon-google-maps', ['q' => ['text', 'כתובת (ריק = כתובת העסק)', '']]],
        'reviews'        => ['reviews', 'reviews', 'ביקורות', 'eicon-review', []],
        'topbar-meta'    => ['topbar-meta', 'topbar_meta', 'פס עליון', 'eicon-info-circle-o', []],
        'nav'            => ['nav', 'nav', 'תפריט ראשי', 'eicon-nav-menu', []],
        'menu'           => ['menu', 'menu', 'תפריט', 'eicon-nav-menu', ['location' => [['footer' => 'פוטר', 'primary' => 'ראשי'], 'מיקום', 'footer']]],
        'footer-contact' => ['footer-contact', 'footer_contact', 'פרטי קשר בפוטר', 'eicon-envelope', []],
        'social'         => ['social', 'social', 'רשתות חברתיות', 'eicon-social-icons', []],
        'copyright'      => ['copyright', 'copyright', 'זכויות יוצרים', 'eicon-text', []],
        'legal'          => ['legal', 'legal', 'קישורים משפטיים', 'eicon-bullet-list', []],
        'group-logo'     => ['group-logo', 'group_logo', 'קרדיט זאפ', 'eicon-image', []],
        'call-line'      => ['call-line', 'call_line', 'שורת טלפון', 'eicon-headphones', []],
        'breadcrumbs'    => ['breadcrumbs', 'breadcrumbs', 'פירורי לחם', 'eicon-yoast', []],
        'phone'          => ['phone', 'phone', 'טלפון', 'eicon-headphones', []],
        'post-title'     => ['post-title', 'post_title', 'כותרת פוסט', 'eicon-post-title', []],
        'post-meta'      => ['post-meta', 'post_meta', 'פרטי פוסט', 'eicon-post-info', []],
        'post-image'     => ['post-image', 'post_image', 'תמונת פוסט', 'eicon-featured-image', []],
        'post-extras'    => ['post-extras', 'post_extras', 'תוספות פוסט', 'eicon-post-content', []],
        'archive-title'  => ['archive-title', 'archive_title', 'כותרת ארכיון', 'eicon-archive-title', []],
        'archive-intro'  => ['archive-intro', 'archive_intro', 'פתיח ארכיון', 'eicon-text', []],
        'archive-posts'  => ['archive-posts', 'archive_posts', 'פוסטים בארכיון', 'eicon-archive-posts', []],
        'page-content'   => ['page-content', 'page_content', 'תוכן העמוד (בטמפלט)', 'eicon-post-content', []],
        'more-posts'     => ['more-posts', 'more_posts', 'מאמרים נוספים', 'eicon-post-list', ['count' => ['number', 'מספר מאמרים', 4]]],
    ];
    $GLOBALS['zap_widget_specs'] = $specs;
    // one small concrete class per widget: Elementor instantiates widgets by class name
    final class Zap_Widget_form extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['form']; } }
    final class Zap_Widget_recent_posts extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['recent-posts']; } }
    final class Zap_Widget_logo extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['logo']; } }
    final class Zap_Widget_nap extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['nap']; } }
    final class Zap_Widget_map extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['map']; } }
    final class Zap_Widget_reviews extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['reviews']; } }
    final class Zap_Widget_topbar_meta extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['topbar-meta']; } }
    final class Zap_Widget_nav extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['nav']; } }
    final class Zap_Widget_menu extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['menu']; } }
    final class Zap_Widget_footer_contact extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['footer-contact']; } }
    final class Zap_Widget_social extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['social']; } }
    final class Zap_Widget_copyright extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['copyright']; } }
    final class Zap_Widget_legal extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['legal']; } }
    final class Zap_Widget_group_logo extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['group-logo']; } }
    final class Zap_Widget_call_line extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['call-line']; } }
    final class Zap_Widget_breadcrumbs extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['breadcrumbs']; } }
    final class Zap_Widget_phone extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['phone']; } }
    final class Zap_Widget_post_title extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['post-title']; } }
    final class Zap_Widget_post_meta extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['post-meta']; } }
    final class Zap_Widget_post_image extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['post-image']; } }
    final class Zap_Widget_post_extras extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['post-extras']; } }
    final class Zap_Widget_archive_title extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['archive-title']; } }
    final class Zap_Widget_archive_intro extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['archive-intro']; } }
    final class Zap_Widget_archive_posts extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['archive-posts']; } }
    final class Zap_Widget_page_content extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['page-content']; } }
    final class Zap_Widget_more_posts extends Zap_Part_Widget { protected static function spec(): array { return $GLOBALS['zap_widget_specs']['more-posts']; } }
    foreach (array_keys($specs) as $n) {
        $cls = 'Zap_Widget_' . str_replace('-', '_', $n);
        $wm->register(new $cls());
    }
});
