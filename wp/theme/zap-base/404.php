<?php defined('ABSPATH') || exit;
get_header(); ?>
<section class="zs-404">
  <div class="zs-wrap zs-wrap--narrow">
    <p class="zs-404__code" aria-hidden="true">404</p>
    <h1>העמוד שחיפשתם לא נמצא</h1>
    <p>ייתכן שהקישור השתנה או שהעמוד הוסר. אפשר לחזור לדף הבית או לפנות אלינו ישירות.</p>
    <p class="zs-404__actions">
      <a class="zs-btn zs-btn--primary" href="<?php echo esc_url(home_url('/')); ?>">לדף הבית</a>
      <?php if ($tel = zs_opt('business.phone_e164')) : ?>
      <a class="zs-btn zs-btn--ghost" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo esc_html(zs_opt('business.phone_display')); ?></a>
      <?php endif; ?>
    </p>
  </div>
</section>
<?php get_footer();
