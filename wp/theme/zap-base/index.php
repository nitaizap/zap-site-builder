<?php defined('ABSPATH') || exit;
/* Blog index, category archives, search and any fallback. */
get_header();
if (is_home()) {
    $pid   = (int) get_option('page_for_posts');
    $title = $pid ? get_the_title($pid) : 'בלוג';
    $intro = $pid ? get_post_field('post_excerpt', $pid) : '';
} elseif (is_search()) {
    $title = 'תוצאות חיפוש: ' . get_search_query();
    $intro = '';
} else {
    $title = wp_strip_all_tags(get_the_archive_title());
    $intro = get_the_archive_description();
}
?>
<section class="zs-archive">
  <div class="zs-wrap">
    <?php zs_breadcrumbs(); ?>
    <h1 class="zs-archive__title"><?php echo esc_html($title); ?></h1>
    <?php if ($intro) : ?><div class="zs-archive__intro"><?php echo wp_kses_post(wpautop($intro)); ?></div><?php endif; ?>
    <?php if (have_posts()) : ?>
    <div class="zs-postgrid">
      <?php while (have_posts()) : the_post(); ?>
      <article class="zs-postcard">
        <a class="zs-postcard__img" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true"><?php if (has_post_thumbnail()) the_post_thumbnail('zs-card'); ?></a>
        <div class="zs-postcard__body">
          <h2 class="zs-postcard__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
          <p><?php echo esc_html(get_the_excerpt()); ?></p>
        </div>
      </article>
      <?php endwhile; ?>
    </div>
    <?php the_posts_pagination(['mid_size' => 1, 'prev_text' => 'הקודם', 'next_text' => 'הבא']); ?>
    <?php else : ?>
    <p>עדיין אין כאן תוכן.</p>
    <?php endif; ?>
  </div>
</section>
<?php get_footer();
