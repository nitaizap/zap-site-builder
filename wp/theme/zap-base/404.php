<?php defined('ABSPATH') || exit;
get_header();
$contact = get_posts(['post_type' => 'page', 'meta_key' => '_zap_page_type', 'meta_value' => 'contact', 'numberposts' => 1]); ?>
<section class="zs-404">
  <div class="zs-wrap zs-wrap--narrow">
    <p class="zs-404__code" aria-hidden="true">404</p>
    <h1>העמוד שחיפשתם לא נמצא</h1>
    <p>ייתכן שהקישור השתנה או שהעמוד הוסר. אפשר לחפש באתר, לחזור לדף הבית או לפנות אלינו ישירות.</p>
    <?php get_search_form(); ?>
    <p class="zs-404__actions">
      <a class="zs-btn zs-btn--primary" href="<?php echo esc_url(home_url('/')); ?>">לדף הבית</a>
      <?php if ($contact) : ?><a class="zs-btn zs-btn--ghost" href="<?php echo esc_url(get_permalink($contact[0])); ?>">צרו קשר</a><?php endif; ?>
      <?php if ($tel = zs_opt('business.phone_e164')) : ?>
      <a class="zs-btn zs-btn--ghost" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo esc_html(zs_opt('business.phone_display')); ?></a>
      <?php endif; ?>
    </p>
    <h2 class="zs-404__h">עמודים מרכזיים</h2>
    <?php wp_nav_menu(['theme_location' => 'primary', 'container' => false, 'menu_class' => 'zs-404__links', 'depth' => 1, 'fallback_cb' => false]); ?>
  </div>
</section>
<?php get_footer();
