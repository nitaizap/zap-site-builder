<?php defined('ABSPATH') || exit;
get_header();
while (have_posts()) : the_post();
    if (get_post_meta(get_the_ID(), '_zs_tpl', true) === 'service' && zs_render_tpl('service')) :
        // shared service-page template (title, excerpt and image of this page; its body via [zap_page_content])
    elseif (zs_is_elementor()) :
        the_content();
    else : ?>
    <div class="zs-wrap zs-page">
      <?php zs_breadcrumbs(); ?>
      <h1 class="zs-page__title"><?php the_title(); ?></h1>
      <div class="zs-prose"><?php the_content(); ?></div>
    </div>
<?php endif;
endwhile;
get_footer();
