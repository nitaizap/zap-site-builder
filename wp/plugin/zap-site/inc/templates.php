<?php defined('ABSPATH') || exit;
/* Shared page templates (Zap QA: "every service page is its own page; a change in one place must update all").
   Service pages and posts render through one Elementor template each (Theme Builder single templates with
   Elementor Pro, saved templates rendered by the theme without it). The template takes the page's own data
   through the dynamic tags below (they render in free Elementor too) and the page body through
   [zap_page_content]. */

add_action('elementor/dynamic_tags/register', function ($tags) {
    $tags->register_group('zap', ['title' => 'Zap']);
    foreach (['Zap_Tag_Title', 'Zap_Tag_Excerpt', 'Zap_Tag_Image'] as $c) $tags->register(new $c());
});

add_action('elementor/init', function () {
    if (!class_exists('\Elementor\Core\DynamicTags\Tag')) return;

    class Zap_Tag_Title extends \Elementor\Core\DynamicTags\Tag {
        public function get_name() { return 'zap-title'; }
        public function get_title() { return 'כותרת העמוד'; }
        public function get_group() { return 'zap'; }
        public function get_categories() { return [\Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY]; }
        public function render() { echo esc_html(get_the_title(zap_tpl_post_id())); }
    }
    class Zap_Tag_Excerpt extends \Elementor\Core\DynamicTags\Tag {
        public function get_name() { return 'zap-excerpt'; }
        public function get_title() { return 'תקציר העמוד'; }
        public function get_group() { return 'zap'; }
        public function get_categories() { return [\Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY]; }
        public function render() { echo esc_html(get_the_excerpt(zap_tpl_post_id())); }
    }
    class Zap_Tag_Image extends \Elementor\Core\DynamicTags\Data_Tag {
        public function get_name() { return 'zap-image'; }
        public function get_title() { return 'התמונה הראשית'; }
        public function get_group() { return 'zap'; }
        public function get_categories() { return [\Elementor\Modules\DynamicTags\Module::IMAGE_CATEGORY]; }
        public function get_value(array $options = []) {
            $id = (int) get_post_thumbnail_id(zap_tpl_post_id());
            return $id ? ['id' => $id, 'url' => wp_get_attachment_image_url($id, 'full')] : [];
        }
    }
});

/** The page or post being shown (also while its template renders). */
function zap_tpl_post_id() {
    $q = get_queried_object_id();
    return $q ?: get_the_ID();
}

/* The page's own Elementor content inside its template (Elementor Pro's Post Content widget does the same). */
add_shortcode('zap_page_content', function () {
    static $depth = 0;
    $id = zap_tpl_post_id();
    if (!$id || $depth > 0) return '';
    $depth++;
    $html = '';
    if (class_exists('\Elementor\Plugin') && \Elementor\Plugin::$instance->documents->get($id) && \Elementor\Plugin::$instance->documents->get($id)->is_built_with_elementor()) {
        // get_builder_content: the _for_display variant returns nothing for the post being shown (its recursion guard)
        $html = \Elementor\Plugin::$instance->frontend->get_builder_content($id, true);
    } else {
        $html = apply_filters('the_content', get_post_field('post_content', $id));
    }
    $depth--;
    return $html;
});

/* A post's body in the post template: the text (images open in a lightbox), its FAQ, the related service. */
add_shortcode('zap_post_body', function () {
    $id = zap_tpl_post_id();
    if (!$id) return '';
    $o = '<div class="zs-prose zs-post__body">' . apply_filters('the_content', get_post_field('post_content', $id)) . '</div>';
    $faq = json_decode((string) get_post_meta($id, '_zap_faq', true), true);
    if ($faq) {
        $o .= '<section class="zs-post__faq zs-faq__list" aria-labelledby="zs-post-faq"><h2 id="zs-post-faq">שאלות נפוצות</h2><div class="elementor-toggle">';
        foreach ($faq as $f) $o .= '<details class="elementor-toggle-item"><summary class="elementor-tab-title">' . esc_html($f['q'] ?? '') . '</summary><div class="elementor-tab-content"><p>' . esc_html($f['a'] ?? '') . '</p></div></details>';
        $o .= '</div></section>';
    }
    $rel = (int) get_post_meta($id, '_zap_related_page', true);
    if ($rel && get_post_status($rel) === 'publish') {
        $o .= '<aside class="zs-post__cta"><p class="zs-post__cta-title">' . esc_html(get_the_title($rel)) . '</p><p>' . esc_html(get_the_excerpt($rel)) . '</p>'
            . '<a class="zs-btn zs-btn--primary" href="' . esc_url(get_permalink($rel)) . '">' . esc_html(get_the_title($rel)) . '</a></aside>';
    }
    return $o;
});

/* Byline under a post's H1. */
add_shortcode('zap_post_meta', function () {
    $id = zap_tpl_post_id();
    $author = zap_opt('business.author_name', zap_opt('business.name'));
    return '<p class="zs-post__meta">מאת ' . esc_html($author) . ' · עודכן <time datetime="' . esc_attr(get_the_modified_date('c', $id)) . '">' . esc_html(get_the_modified_date('', $id)) . '</time></p>';
});

/* "מאמרים נוספים": the other posts as a side list. */
add_shortcode('zap_more_posts', function ($atts) {
    $a = shortcode_atts(['count' => 4], $atts);
    $q = new WP_Query(['post_type' => 'post', 'posts_per_page' => (int) $a['count'], 'post__not_in' => [zap_tpl_post_id()], 'ignore_sticky_posts' => true, 'no_found_rows' => true]);
    if (!$q->have_posts()) return '';
    $o = '<ul class="zs-moreposts">';
    while ($q->have_posts()) {
        $q->the_post();
        $o .= '<li><a href="' . esc_url(get_permalink()) . '">' . (has_post_thumbnail() ? get_the_post_thumbnail(null, 'thumbnail', ['loading' => 'lazy', 'alt' => get_the_title()]) : '')
            . '<span>' . esc_html(get_the_title()) . '</span></a></li>';
    }
    wp_reset_postdata();
    return $o . '</ul>';
});
