<?php defined('ABSPATH') || exit;
get_header();
while (have_posts()) : the_post();
    $author  = zs_opt('business.author_name', zs_opt('business.name'));
    $credit  = zs_opt('business.author_credentials');
    $related = (int) get_post_meta(get_the_ID(), '_zap_related_page', true);
    $cats    = get_the_category(); ?>
<article class="zs-post">
  <header class="zs-post__head">
    <div class="zs-wrap zs-wrap--narrow">
      <?php zs_breadcrumbs(); ?>
      <?php if ($cats) : ?><a class="zs-eyebrow" href="<?php echo esc_url(get_category_link($cats[0])); ?>"><?php echo esc_html($cats[0]->name); ?></a><?php endif; ?>
      <h1 class="zs-post__title"><?php the_title(); ?></h1>
      <p class="zs-post__meta">מאת <?php echo esc_html($author); ?> · עודכן <time datetime="<?php echo esc_attr(get_the_modified_date('c')); ?>"><?php echo esc_html(get_the_modified_date()); ?></time></p>
    </div>
  </header>
  <?php if (has_post_thumbnail()) : ?>
  <figure class="zs-wrap zs-wrap--narrow zs-post__hero"><?php the_post_thumbnail('zs-wide', ['loading' => 'eager', 'fetchpriority' => 'high']); ?></figure>
  <?php endif; ?>
  <div class="zs-wrap zs-wrap--narrow zs-prose"><?php the_content(); ?></div>
  <div class="zs-wrap zs-wrap--narrow">
    <?php if ($related && get_post_status($related) === 'publish') : ?>
    <aside class="zs-post__cta">
      <p class="zs-post__cta-title"><?php echo esc_html(get_the_title($related)); ?></p>
      <p><?php echo esc_html(get_the_excerpt($related)); ?></p>
      <a class="zs-btn zs-btn--primary" href="<?php echo esc_url(get_permalink($related)); ?>"><?php echo esc_html(get_the_title($related)); ?></a>
    </aside>
    <?php endif; ?>
    <aside class="zs-author">
      <p class="zs-author__name"><?php echo esc_html($author); ?></p>
      <?php if ($credit) : ?><p><?php echo esc_html($credit); ?></p><?php endif; ?>
    </aside>
    <?php if ($d = zs_opt('content.disclaimer')) : ?><p class="zs-disclaimer"><?php echo esc_html($d); ?></p><?php endif; ?>
  </div>
</article>
<?php endwhile;
get_footer();
