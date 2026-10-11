<?php defined('ABSPATH') || exit;
$name    = zs_opt('business.name', get_bloginfo('name'));
$phone   = zs_opt('business.phone_display');
$tel     = zs_opt('business.phone_e164');
$wa      = zs_opt('business.whatsapp_e164');
$wa_text = zs_opt('business.whatsapp_text', 'שלום, הגעתי מהאתר ואשמח לפרטים');
$address = zs_opt('business.address');
$hours   = (array) zs_opt('business.hours', []);
$about   = zs_opt('footer.about');
$privacy = zs_opt('standards.privacy_url', home_url('/מדיניות-פרטיות/'));
$a11y    = zs_opt('standards.accessibility_url', 'https://zap.dbusiness.co/js/accessibility.html');
$is_contact = is_page() && get_post_meta(get_the_ID(), '_zap_page_type', true) === 'contact';
?>
</main>
<?php if (!zs_render_tpl('footer')) : ?>
<?php if (!$is_contact && shortcode_exists('zap_form')) : ?>
<section class="zs-leadband" id="leave-details" aria-labelledby="zs-leadband-title">
  <div class="zs-wrap zs-leadband__in">
    <div class="zs-leadband__text">
      <h2 id="zs-leadband-title"><?php echo esc_html(zs_opt('form.title', 'השאירו פרטים ונחזור אליכם')); ?></h2>
      <p><?php echo esc_html(zs_opt('form.text', 'ממלאים שם וטלפון, ואנחנו חוזרים בהקדם.')); ?></p>
      <?php echo zs_part_call_line(); ?>
    </div>
    <?php echo do_shortcode('[zap_form id="footer"]'); ?>
  </div>
</section>
<?php endif; ?>
<footer class="zs-footer">
  <div class="zs-wrap zs-footer__grid">
    <div class="zs-footer__col zs-footer__brand">
      <p class="zs-footer__name"><?php echo esc_html($name); ?></p>
      <?php if ($about) : ?><p><?php echo esc_html($about); ?></p><?php endif; ?>
    </div>
    <?php if (has_nav_menu('footer')) : ?>
    <nav class="zs-footer__col" aria-labelledby="zs-f-links">
      <h2 class="zs-footer__title" id="zs-f-links"><?php echo esc_html(zs_opt('footer.links_title', 'השירותים שלנו')); ?></h2>
      <?php echo zs_part_menu('footer'); ?>
    </nav>
    <?php endif; ?>
    <div class="zs-footer__col">
      <h2 class="zs-footer__title">יצירת קשר</h2>
      <?php echo zs_part_footer_contact(); ?>
    </div>
  </div>
  <div class="zs-footer__mark" aria-hidden="true"><?php echo esc_html($name); ?></div>
  <div class="zs-footer__bar">
    <div class="zs-wrap zs-footer__bar-in">
      <?php echo zs_part_copyright(); ?>
      <?php echo zs_part_legal(); ?>
      <?php echo zs_part_group_logo(); ?>
    </div>
  </div>
</footer>
<?php endif; ?>
<?php if ($tel || $wa) : ?>
<div class="zs-fab" aria-label="יצירת קשר מהירה">
  <?php if ($tel) : ?><a class="zs-fab__call" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo zs_icon('phone'); ?><span>התקשרו</span></a><?php endif; ?>
  <?php if ($wa) : ?><a class="zs-fab__wa" href="<?php echo esc_url(zs_wa_href($wa, $wa_text)); ?>" target="_blank" rel="noopener"><?php echo zs_icon('whatsapp'); ?><span>וואטסאפ</span></a><?php endif; ?>
</div>
<?php endif; ?>
<?php wp_footer(); ?>
</body>
</html>
