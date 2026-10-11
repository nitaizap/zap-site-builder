<?php
/** Shortcodes the Elementor pages embed for dynamic or shared parts. */
defined('ABSPATH') || exit;

/* Latest blog posts as cards. [zap_recent_posts count="3" category="slug"] */
add_shortcode('zap_recent_posts', function ($atts) {
    $a = shortcode_atts(['count' => 3, 'category' => '', 'exclude' => ''], $atts);
    $q = new WP_Query([
        'post_type'           => 'post',
        'posts_per_page'      => (int) $a['count'],
        'category_name'       => $a['category'],
        'post__not_in'        => array_filter(array_map('intval', explode(',', $a['exclude']))),
        'ignore_sticky_posts' => true,
        'no_found_rows'       => true,
    ]);
    if (!$q->have_posts()) return '';
    ob_start();
    echo '<div class="zs-postgrid">';
    while ($q->have_posts()) {
        $q->the_post(); ?>
      <article class="zs-postcard">
        <a class="zs-postcard__img" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true"><?php if (has_post_thumbnail()) the_post_thumbnail('zs-card', ['loading' => 'lazy']); ?></a>
        <div class="zs-postcard__body">
          <h3 class="zs-postcard__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
          <p><?php echo esc_html(get_the_excerpt()); ?></p>
        </div>
      </article>
    <?php }
    echo '</div>';
    wp_reset_postdata();
    return ob_get_clean();
});

/* Dapei Zahav reviews: renders only with a real customer-id. */
add_shortcode('zap_reviews', function () {
    $cid = preg_replace('/\D/', '', (string) zap_opt('business.dpz_customer_id'));
    if (!$cid) return '';
    wp_enqueue_script('zap-reviews', 'https://zap.dbusiness.co/js/zap-reviews.js', [], null, ['strategy' => 'defer', 'in_footer' => true]);
    wp_enqueue_script('zap-score', 'https://zap.dbusiness.co/js/zap-score.js', [], null, ['strategy' => 'defer', 'in_footer' => true]);
    wp_enqueue_style('zap-reviews', 'https://zap.dbusiness.co/css/zap-reviews.css', [], null);
    wp_enqueue_style('zap-reviews-dpz', 'https://zap.dbusiness.co/css/zap-reviews-dpz.css', [], null);
    return '<div class="zs-reviews"><zap-reviews customer-id="' . esc_attr($cid) . '" site-id="5"></zap-reviews>'
        . '<p class="zs-reviews__links"><a href="https://www.d.co.il/' . esc_attr($cid) . '/" target="_blank" rel="noopener">לכל הביקורות בדפי זהב</a></p></div>';
});

/* Map by address, no API key. */
add_shortcode('zap_map', function ($atts) {
    $a = shortcode_atts(['q' => zap_opt('business.address')], $atts);
    if (!$a['q']) return '';
    $src = 'https://www.google.com/maps?q=' . rawurlencode($a['q']) . '&output=embed&hl=iw';
    return '<div class="zs-map"><iframe src="' . esc_url($src) . '" title="מפת הגעה — ' . esc_attr(zap_opt('business.name')) . '" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>';
});

/* Business contact details block. */
add_shortcode('zap_nap', function () {
    $b = zap_opt('business', []);
    $o = '<ul class="zs-nap">';
    if (!empty($b['phone_e164'])) $o .= '<li>' . zs_icon('phone') . '<a href="' . esc_attr(zs_tel_href($b['phone_e164'])) . '">' . esc_html($b['phone_display']) . '</a></li>';
    if (!empty($b['whatsapp_e164'])) $o .= '<li>' . zs_icon('whatsapp') . '<a href="' . esc_url(zs_wa_href($b['whatsapp_e164'], zap_opt('business.whatsapp_text', 'שלום, הגעתי מהאתר ואשמח לפרטים'))) . '" target="_blank" rel="noopener">וואטסאפ</a></li>';
    if (!empty($b['email_public'])) $o .= '<li>' . zs_icon('mail') . '<a href="mailto:' . esc_attr($b['email_public']) . '">' . esc_html($b['email_public']) . '</a></li>';
    if (!empty($b['address'])) $o .= '<li>' . zs_icon('pin') . '<span>' . esc_html($b['address']) . '</span></li>';
    foreach ((array) ($b['hours'] ?? []) as $h) $o .= '<li>' . zs_icon('clock') . '<span>' . esc_html($h) . '</span></li>';
    return $o . '</ul>';
});

add_shortcode('zap_breadcrumbs', function () {
    if (!function_exists('yoast_breadcrumb') || is_front_page()) return '';
    return yoast_breadcrumb('<nav class="zs-crumbs" aria-label="פירורי לחם">', '</nav>', false);
});

add_shortcode('zap_phone', function () {
    $t = zap_opt('business.phone_e164');
    return $t ? '<a href="' . esc_attr(zs_tel_href($t)) . '">' . esc_html(zap_opt('business.phone_display')) . '</a>' : '';
});
