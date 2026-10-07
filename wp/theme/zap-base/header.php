<?php defined('ABSPATH') || exit;
$name  = zs_opt('business.name', get_bloginfo('name'));
$phone = zs_opt('business.phone_display');
$tel   = zs_opt('business.phone_e164');
$cta   = zs_opt('header.cta_label', '');
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="zs-skip" href="#content">דלג לתוכן הראשי</a>
<header class="zs-header" id="top">
  <div class="zs-wrap zs-header__in">
    <a class="zs-brand" href="<?php echo esc_url(home_url('/')); ?>" rel="home" aria-label="<?php echo esc_attr($name); ?> - דף הבית">
      <?php
      $logo_id = get_theme_mod('custom_logo');
      if ((zs_design()['header'] ?? 'light') === 'dark' && zs_opt('logo_light_id')) $logo_id = (int) zs_opt('logo_light_id');
      if ($logo_id) {
          echo wp_get_attachment_image($logo_id, 'full', false, ['class' => 'zs-brand__logo', 'alt' => $name, 'loading' => 'eager', 'fetchpriority' => 'high', 'decoding' => 'async']);
      } else {
          echo '<span class="zs-brand__name">' . esc_html($name) . '</span>';
      }
      ?>
    </a>
    <nav id="zs-nav" class="zs-nav" aria-label="תפריט ראשי">
      <?php wp_nav_menu([
          'theme_location' => 'primary',
          'container'      => false,
          'menu_class'     => 'zs-menu',
          'depth'          => 2,
          'fallback_cb'    => false,
      ]); ?>
      <?php if ($tel) : ?>
      <a class="zs-btn zs-btn--primary zs-nav__cta" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo zs_icon('phone'); ?><span><?php echo esc_html($cta ?: $phone); ?></span></a>
      <?php endif; ?>
    </nav>
    <?php if ($tel) : ?>
    <a class="zs-btn zs-btn--primary zs-header__cta" href="<?php echo esc_attr(zs_tel_href($tel)); ?>"><?php echo zs_icon('phone'); ?><span><?php echo esc_html($phone); ?></span></a>
    <?php endif; ?>
    <button class="zs-burger" type="button" aria-expanded="false" aria-controls="zs-nav" aria-label="פתיחת תפריט"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="content" class="zs-main" tabindex="-1">
