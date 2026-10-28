<?php defined('ABSPATH') || exit;
/* Search results (SEO checklist #30): the query, a new search box and the matching posts and pages. */
get_header(); ?>
<section class="zs-search">
  <div class="zs-wrap zs-wrap--narrow">
    <h1>תוצאות חיפוש: <?php echo esc_html(get_search_query()); ?></h1>
    <?php get_search_form(); ?>
    <?php if (have_posts()) : ?>
    <ul class="zs-search__list">
      <?php while (have_posts()) : the_post(); ?>
      <li><h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2><p><?php echo esc_html(wp_trim_words(get_the_excerpt(), 28)); ?></p></li>
      <?php endwhile; ?>
    </ul>
    <?php the_posts_pagination(); ?>
    <?php else : ?>
    <p>לא נמצאו תוצאות. נסו מילה אחרת או חזרו <a href="<?php echo esc_url(home_url('/')); ?>">לדף הבית</a>.</p>
    <?php endif; ?>
  </div>
</section>
<?php get_footer();
