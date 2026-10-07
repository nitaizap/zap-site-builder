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
<?php if (!$is_contact && shortcode_exists('zap_form')) : ?>
<section class="zs-leadband" id="leave-details" aria-labelledby="zs-leadband-title">
  <div class="zs-wrap zs-leadband__in">
    <div class="zs-leadband__text">
      <h2 id="zs-leadband-title"><?php echo esc_html(zs_opt('form.title', 'השאירו פרטים ונחזור אליכם')); ?></h2>
      <p><?php echo esc_html(zs_opt('form.text', 'ממלאים שם וטלפון, ואנחנו חוזרים בהקדם.')); ?></p>
      <?php if ($tel) : ?><p class="zs-leadband__or">או התקשרו: <a href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo esc_html($phone); ?></a></p><?php endif; ?>
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
      <?php wp_nav_menu(['theme_location' => 'footer', 'container' => false, 'menu_class' => 'zs-footer__links', 'depth' => 1]); ?>
    </nav>
    <?php endif; ?>
    <div class="zs-footer__col">
      <h2 class="zs-footer__title">יצירת קשר</h2>
      <ul class="zs-footer__contact">
        <?php if ($tel) : ?><li><?php echo zs_icon('phone'); ?><a href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo esc_html($phone); ?></a></li><?php endif; ?>
        <?php if ($wa) : ?><li><?php echo zs_icon('whatsapp'); ?><a href="<?php echo esc_url(zs_wa_href($wa, $wa_text)); ?>" target="_blank" rel="noopener">שלחו הודעת וואטסאפ</a></li><?php endif; ?>
        <?php if ($address) : ?><li><?php echo zs_icon('pin'); ?><span><?php echo esc_html($address); ?></span></li><?php endif; ?>
        <?php foreach ($hours as $h) : ?><li><?php echo zs_icon('clock'); ?><span><?php echo esc_html($h); ?></span></li><?php endforeach; ?>
      </ul>
    </div>
  </div>
  <div class="zs-footer__bar">
    <div class="zs-wrap zs-footer__bar-in">
      <p>© <?php echo esc_html(date('Y') . ' ' . $name); ?> — כל הזכויות שמורות<?php if (zs_opt('footer.ai_images_note')) echo ' · ' . esc_html(zs_opt('footer.ai_images_note')); ?></p>
      <ul class="zs-footer__legal">
        <li><a href="<?php echo esc_url($privacy); ?>">מדיניות פרטיות</a></li>
        <li><a href="<?php echo esc_url($a11y); ?>" target="_blank" rel="noopener">הצהרת נגישות אתר</a></li>
      </ul>
      <a class="zs-footer__zap" href="https://zapgroup.co.il/" target="_blank" rel="noopener">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/zap-group.webp'); ?>" width="183" height="26" alt="זאפ גרופ" loading="lazy" decoding="async">
      </a>
    </div>
  </div>
</footer>
<?php if ($tel || $wa) : ?>
<div class="zs-fab" aria-label="יצירת קשר מהירה">
  <?php if ($tel) : ?><a class="zs-fab__call" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo zs_icon('phone'); ?><span>התקשרו</span></a><?php endif; ?>
  <?php if ($wa) : ?><a class="zs-fab__wa" href="<?php echo esc_url(zs_wa_href($wa, $wa_text)); ?>" target="_blank" rel="noopener"><?php echo zs_icon('whatsapp'); ?><span>וואטסאפ</span></a><?php endif; ?>
</div>
<?php endif; ?>
<?php wp_footer(); ?>
</body>
</html>
