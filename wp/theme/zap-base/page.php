<?php defined('ABSPATH') || exit;
get_header();
while (have_posts()) : the_post();
    if (zs_is_elementor()) :
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
