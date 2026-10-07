<?php
/**
 * One lead form for the whole site. Every submission is saved first, then emailed.
 * Anti-bot: honeypot + HMAC time token + content signals. A missing token never blocks:
 * a browser that didn't run our markup is still a customer.
 */
defined('ABSPATH') || exit;

add_action('init', function () {
    register_post_type('zap_lead', [
        'labels'        => ['name' => 'פניות מהאתר', 'singular_name' => 'פנייה', 'menu_name' => 'פניות מהאתר'],
        'public'        => false,
        'show_ui'       => true,
        'show_in_menu'  => true,
        'menu_icon'     => 'dashicons-email-alt',
        'menu_position' => 3,
        'supports'      => ['title', 'editor'],
        'capabilities'  => ['create_posts' => 'do_not_allow'],
        'map_meta_cap'  => true,
    ]);
});

function zap_form_token() {
    $t = (string) time();
    return $t . '.' . substr(hash_hmac('sha256', $t, wp_salt('nonce')), 0, 20);
}

function zap_form_token_age($token) {
    if (!preg_match('/^(\d{9,11})\.([a-f0-9]{20})$/', (string) $token, $m)) return null;
    $ok = hash_equals(substr(hash_hmac('sha256', $m[1], wp_salt('nonce')), 0, 20), $m[2]);
    return $ok ? time() - (int) $m[1] : null;
}

add_shortcode('zap_form', function ($atts) {
    $a = shortcode_atts(['id' => 'main', 'message' => 'yes', 'email' => 'no', 'button' => ''], $atts);
    $uid = 'zf-' . sanitize_key($a['id']);
    $privacy = zap_opt('standards.privacy_url', home_url('/מדיניות-פרטיות/'));
    $button = $a['button'] ?: zap_opt('form.button', 'שליחה');
    $sent = isset($_GET['zs_sent']) && $_GET['zs_sent'] === $a['id'];
    ob_start(); ?>
<form class="zs-form" id="<?php echo esc_attr($uid); ?>" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
  <?php if ($sent) : ?>
  <p class="zs-form__ok" role="status"><?php echo esc_html(zap_opt('form.thanks', 'תודה! הפרטים התקבלו ונחזור אליכם בהקדם.')); ?></p>
  <?php endif; ?>
  <?php if (!$sent && isset($_GET['zs_err'])) : ?>
  <p class="zs-form__err" role="alert">נא למלא שם ומספר טלפון תקין.</p>
  <?php endif; ?>
  <input type="hidden" name="action" value="zap_lead">
  <input type="hidden" name="zf_form" value="<?php echo esc_attr($a['id']); ?>">
  <input type="hidden" name="zf_token" value="<?php echo esc_attr(zap_form_token()); ?>">
  <div class="zs-form__hp" aria-hidden="true"><label>אתר אינטרנט<input type="text" name="zf_website" tabindex="-1" autocomplete="off"></label></div>
  <div class="zs-form__row">
    <p class="zs-field"><label for="<?php echo $uid; ?>-name">שם מלא</label><input id="<?php echo $uid; ?>-name" name="zf_name" type="text" required autocomplete="name"></p>
    <p class="zs-field"><label for="<?php echo $uid; ?>-phone">טלפון</label><input id="<?php echo $uid; ?>-phone" name="zf_phone" type="tel" required autocomplete="tel" inputmode="tel" pattern="[0-9+\-\s()]{9,16}" dir="ltr"></p>
    <?php if ($a['email'] === 'yes') : ?>
    <p class="zs-field"><label for="<?php echo $uid; ?>-email">אימייל</label><input id="<?php echo $uid; ?>-email" name="zf_email" type="email" autocomplete="email" dir="ltr"></p>
    <?php endif; ?>
  </div>
  <?php if ($a['message'] === 'yes') : ?>
  <p class="zs-field"><label for="<?php echo $uid; ?>-msg">במה נוכל לעזור?</label><textarea id="<?php echo $uid; ?>-msg" name="zf_message" rows="3"></textarea></p>
  <?php endif; ?>
  <p class="zs-form__consent"><label><input type="checkbox" name="zf_consent" value="1" required> אני מאשר/ת את <a href="<?php echo esc_url($privacy); ?>" target="_blank" rel="noopener">מדיניות הפרטיות</a></label></p>
  <p><button class="zs-btn zs-btn--primary zs-form__submit" type="submit"><?php echo esc_html($button); ?></button></p>
</form>
<?php return ob_get_clean();
});

add_action('admin_post_nopriv_zap_lead', 'zap_handle_lead');
add_action('admin_post_zap_lead', 'zap_handle_lead');

function zap_handle_lead() {
    $f = fn($k) => isset($_POST[$k]) ? trim(wp_unslash((string) $_POST[$k])) : '';
    $form    = sanitize_key($f('zf_form')) ?: 'main';
    $name    = sanitize_text_field($f('zf_name'));
    $phone   = sanitize_text_field($f('zf_phone'));
    $email   = sanitize_email($f('zf_email'));
    $message = sanitize_textarea_field($f('zf_message'));
    $back    = wp_get_referer() ?: home_url('/');
    $back    = remove_query_arg('zs_sent', $back);

    $why = '';
    $age = zap_form_token_age($f('zf_token'));
    if ($f('zf_website') !== '')                       $why = 'honeypot';
    elseif ($age !== null && $age < 3)                 $why = 'too-fast';
    elseif ($age !== null && $age > 6 * HOUR_IN_SECONDS) $why = 'stale-token';
    elseif (preg_match('~https?://|www\.~i', $message)) $why = 'link-in-message';
    elseif (preg_match('/\p{Cyrillic}/u', $name . $phone)) $why = 'cyrillic';
    elseif ($name === '' || !preg_match('/\d{7,}/', preg_replace('/\D/', '', $phone))) $why = 'missing-fields';

    if ($why) {
        $log = get_option('zap_lead_blocks', []);
        array_unshift($log, ['t' => current_time('mysql'), 'why' => $why, 'name' => $name, 'phone' => $phone]);
        update_option('zap_lead_blocks', array_slice($log, 0, 50), false);
        if ($why === 'missing-fields') {
            wp_safe_redirect(add_query_arg('zs_err', '1', $back) . '#zf-' . $form);
            exit;
        }
        // Bots get the same thank-you page as people.
        wp_safe_redirect(add_query_arg('zs_sent', $form, $back) . '#zf-' . $form);
        exit;
    }

    $page = esc_url_raw($back);
    $lines = array_filter([
        "שם: $name",
        "טלפון: $phone",
        $email ? "אימייל: $email" : '',
        $message ? "הודעה: $message" : '',
        "עמוד: " . urldecode($page),
        'זמן: ' . current_time('d/m/Y H:i'),
        $age === null ? 'הערה: הטופס נשלח ללא טוקן (ייתכן דפדפן ישן)' : '',
    ]);
    $body = implode("\n", $lines);

    $id = wp_insert_post([
        'post_type'    => 'zap_lead',
        'post_status'  => 'private',
        'post_title'   => "$name · $phone",
        'post_content' => $body,
    ]);
    update_post_meta($id, '_zap_form', $form);

    $to = zap_opt('business.email_leads');
    // Never mail the client from a staging build: leads are saved, mail starts on the live site.
    // An internal address can receive test mail meanwhile (zap_site.smtp.test_to).
    if (wp_get_environment_type() !== 'production') {
        $to = zap_opt('smtp.test_to');
        if (!$to) update_post_meta($id, '_zap_mailed', 'staging-skip');
    }
    if ($to) {
        $headers = [];
        if ($email) $headers[] = 'Reply-To: ' . $name . ' <' . $email . '>';
        $subject = 'פנייה חדשה מהאתר — ' . zap_opt('business.name', get_bloginfo('name'));
        $ok = wp_mail($to, $subject, $body, $headers);
        update_post_meta($id, '_zap_mailed', $ok ? 'yes' : 'no');
    }
    wp_safe_redirect(add_query_arg('zs_sent', $form, $back) . '#zf-' . $form);
    exit;
}

/* ---------- mail: Zap relay, Zap sender ---------- */
add_filter('wp_mail_from', fn() => zap_opt('smtp.from', 'zapsites@d.co.il'));
add_filter('wp_mail_from_name', fn() => zap_opt('business.name', get_bloginfo('name')));
add_action('phpmailer_init', function ($m) {
    if (!zap_opt('smtp.enabled', true)) return;
    $m->isSMTP();
    $m->Host = zap_opt('smtp.host', 'relay.d.co.il');
    $m->Port = (int) zap_opt('smtp.port', 25);
    $m->SMTPAuth = false;
    $m->SMTPSecure = '';      // relay offers no TLS; forcing it fails every send
    $m->SMTPAutoTLS = false;
    $m->Timeout = 10;
});
