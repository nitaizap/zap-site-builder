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
    if (!zap_opt('business.email_leads')) return '';   // calls-only site: no inbox for leads, so no form
    // the contact page has its own full form; the site-wide footer form stays out of its markup
    if ($a['id'] === 'footer' && is_page() && get_post_meta(get_the_ID(), '_zap_page_type', true) === 'contact') return '';
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
  <p class="zs-form__consent"><label><input type="checkbox" name="zf_consent" value="1" required> <span>אני מאשר/ת את <a href="<?php echo esc_url($privacy); ?>" target="_blank" rel="noopener">מדיניות הפרטיות</a></span></label></p>
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
    // staging = the site's address (inc/launch.php), never a database flag that a migration would carry to the live site
    if (zap_is_staging()) {
        $to = zap_opt('smtp.test_to');
        if (!$to) update_post_meta($id, '_zap_mailed', 'staging-skip');
    }
    if ($to) {
        $headers = [];
        if ($email) $headers[] = 'Reply-To: ' . $name . ' <' . $email . '>';
        $subject = 'פנייה חדשה מהאתר: ' . zap_opt('business.name', get_bloginfo('name'));
        $ok = zap_send_plugin_mail($to, $subject, $body, $headers);
        update_post_meta($id, '_zap_mailed', $ok ? 'yes' : 'no');
    }
    wp_safe_redirect(add_query_arg('zs_sent', $form, $back) . '#zf-' . $form);
    exit;
}

/* ---------- mail: the Zap relay, used only for the mail THIS plugin sends ----------
 *
 * History: this block used to hook `wp_mail_from`, `wp_mail_from_name` and `phpmailer_init` globally, at the
 * default priority 10, with the relay on by default. Three consequences, all of them reported as "בעיות SMTP":
 *   1. every wp_mail on the site (password resets, WooCommerce, any other plugin) was forced through
 *      relay.d.co.il:25, unauthenticated and without TLS;
 *   2. priority 10 is also where WP Mail SMTP, FluentSMTP, Post SMTP and the rest configure PHPMailer, so which
 *      one won depended on plugin load order: the same site could deliver or not deliver after an unrelated
 *      plugin update;
 *   3. every message left as zapsites@d.co.il, a domain the client's site has no SPF/DKIM alignment with, so
 *      mail that did go out landed in spam.
 *
 * Now: another mailer always wins (we stand down completely and say so in wp-admin), the relay and the sender
 * filters are attached around our own send only and removed again afterwards, and the sender is an address on
 * the site's own domain with the enquirer as Reply-To.
 */

/** Mailer plugins that take wp_mail over. plugin-folder => the name an admin recognises. */
function zap_known_mailers() {
    return [
        'wp-mail-smtp'                       => 'WP Mail SMTP',
        'wp-mail-smtp-pro'                   => 'WP Mail SMTP Pro',
        'fluent-smtp'                        => 'FluentSMTP',
        'post-smtp'                          => 'Post SMTP',
        'easy-wp-smtp'                       => 'Easy WP SMTP',
        'wp-ses'                             => 'WP Offload SES',
        'amazon-ses-for-wordpress'           => 'WP Offload SES',
        'mailin'                             => 'Brevo (Sendinblue)',
        'sendinblue-for-woocommerce'         => 'Brevo (Sendinblue)',
        'sendgrid-email-delivery-simplified' => 'SendGrid',
        'wp-sendgrid-mailer'                 => 'SendGrid',
        'mailgun'                            => 'Mailgun',
        'wp-mailgun-smtp'                    => 'Mailgun',
        'smtp-mailer'                        => 'SMTP Mailer',
        'wp-smtp'                            => 'WP SMTP',
        'gmail-smtp'                         => 'Gmail SMTP',
        'postman-smtp'                       => 'Postman SMTP',
    ];
}

/** Plugin folders active on this site (single site + network). */
function zap_active_plugin_dirs() {
    $files = (array) get_option('active_plugins', []);
    if (is_multisite()) $files = array_merge($files, array_keys((array) get_site_option('active_sitewide_plugins', [])));
    $dirs = [];
    foreach ($files as $f) {
        $f = (string) $f;
        $d = strtok($f, '/');
        if ($d && $d !== $f) $dirs[$d] = true;   // "folder/file.php"; a single-file plugin has no folder
    }
    return array_keys($dirs);
}

/** How many callbacks other than ours are attached to phpmailer_init. */
function zap_other_phpmailer_hooks() {
    global $wp_filter;
    if (empty($wp_filter['phpmailer_init'])) return 0;
    $n = 0;
    foreach ($wp_filter['phpmailer_init'] as $cbs) {
        foreach ((array) $cbs as $cb) {
            $fn = is_array($cb) ? ($cb['function'] ?? null) : null;
            if (is_string($fn) && $fn === 'zap_mail_relay') continue;
            $n++;
        }
    }
    return $n;
}

/**
 * Who is managing mail on this site, if it is not us.
 * '' = nobody else, so our relay may run. Otherwise a name to show an admin.
 * Two independent signals: a known mailer plugin is active, or something other than us is already on phpmailer_init.
 */
function zap_foreign_mailer() {
    $known = zap_known_mailers();
    $hits = [];
    foreach (zap_active_plugin_dirs() as $dir) {
        if (isset($known[$dir])) $hits[$known[$dir]] = true;
    }
    if ($hits) return implode(', ', array_keys($hits));
    // a mailer configured in an mu-plugin, a snippet or a host drop-in leaves no plugin row, but it does leave a hook
    $n = zap_other_phpmailer_hooks();
    if ($n) return sprintf('תוסף או קוד אחר (%d חיבורים ל-phpmailer_init)', $n);
    return '';
}

/** The address we send AS: the client's own domain, so SPF/DMARC can align. zapsites@d.co.il only as a last resort. */
function zap_mail_from_address() {
    $set = zap_opt('smtp.from');            // a site that configured one explicitly keeps it
    if ($set) return $set;
    $host = strtolower((string) parse_url(home_url(), PHP_URL_HOST));
    $host = preg_replace('/^www\./', '', strtok($host, ':'));
    // a real domain only: never "localhost", an IP, a single label or a staging address
    if ($host && !filter_var($host, FILTER_VALIDATE_IP) && substr_count($host, '.') >= 1 && !zap_is_staging_host($host)) {
        return 'no-reply@' . $host;
    }
    return 'zapsites@d.co.il';
}

/** Is our relay going to run at all? [bool active, string reason in Hebrew, string mailer-in-charge]. */
function zap_mail_relay_state() {
    $other = zap_foreign_mailer();
    if ($other) {
        return [false, 'מערכת דואר אחרת מנהלת את השליחה באתר: ' . $other . '. ממסר זאפ מושבת אוטומטית והשליחה נשארת שלה.', $other];
    }
    if (!zap_opt('smtp.enabled', true)) {
        return [false, 'ממסר הדואר של זאפ כבוי בהגדרות (smtp.enabled). המיילים נשלחים בדרך הרגילה של ההוסטינג.', 'WordPress (wp_mail)'];
    }
    return [true, 'ממסר זאפ פעיל, ורק עבור מיילים של טופס הפניות: ' . zap_opt('smtp.host', 'relay.d.co.il') . ':' . (int) zap_opt('smtp.port', 25) . '.', 'Zap Site'];
}

/** Record the decision where an admin can read it (settings screen) and a log reader can find it. */
function zap_mail_log_decision($active, $why) {
    $prev = get_option('zap_mail_decision', []);
    if (($prev['active'] ?? null) === (bool) $active && ($prev['why'] ?? null) === $why) return;
    update_option('zap_mail_decision', ['t' => current_time('mysql'), 'active' => (bool) $active, 'why' => $why], false);
    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log('[zap-site] mail: ' . ($active ? 'relay active' : 'relay stood down') . ' - ' . $why);
    }
}

/** Our PHPMailer configuration. Named (not a closure) so zap_other_phpmailer_hooks can tell it apart. */
function zap_mail_relay($m) {
    if (empty($GLOBALS['zap_sending_lead'])) return;      // our own mail only: never the whole site's
    [$active, $why] = zap_mail_relay_state();
    zap_mail_log_decision($active, $why);
    if (!$active) return;                                 // another mailer's configured delivery always wins
    $m->isSMTP();
    $m->Host = zap_opt('smtp.host', 'relay.d.co.il');
    $m->Port = (int) zap_opt('smtp.port', 25);
    $m->SMTPAuth = false;
    $m->SMTPSecure = '';      // relay offers no TLS; forcing it fails every send
    $m->SMTPAutoTLS = false;
    $m->Timeout = 10;
}
// late, so a mailer that registers after us is already visible when we decide whether to stand down
add_action('phpmailer_init', 'zap_mail_relay', 1000);

function zap_mail_from_filter() { return zap_mail_from_address(); }
function zap_mail_from_name_filter() { return zap_opt('business.name', get_bloginfo('name')); }

/** Send one message as the plugin: the sender filters and the relay apply here and nowhere else. */
function zap_send_plugin_mail($to, $subject, $body, $headers = []) {
    $GLOBALS['zap_sending_lead'] = true;
    add_filter('wp_mail_from', 'zap_mail_from_filter', 1000);
    add_filter('wp_mail_from_name', 'zap_mail_from_name_filter', 1000);
    try {
        return wp_mail($to, $subject, $body, $headers);
    } finally {
        remove_filter('wp_mail_from', 'zap_mail_from_filter', 1000);
        remove_filter('wp_mail_from_name', 'zap_mail_from_name_filter', 1000);
        unset($GLOBALS['zap_sending_lead']);
    }
}

/** The decision, recomputed on an admin screen so the settings page is never stale. */
function zap_mail_status_line() {
    [$active, $why, $who] = zap_mail_relay_state();
    zap_mail_log_decision($active, $why);
    return [$active, $why, $who];
}

/* ---------- where the leads go: a settings screen under "פניות מהאתר" (Zap QA asked where the form e-mail is set) ---------- */
add_action('admin_menu', function () {
    add_submenu_page('edit.php?post_type=zap_lead', 'הגדרות טפסים', 'הגדרות טפסים', 'manage_options', 'zap-form-settings', 'zap_form_settings_page');
});

function zap_form_settings_page() {
    if (!current_user_can('manage_options')) return;
    $staging = zap_is_staging();
    $saved = isset($_GET['saved']);
    [$relay_on, $relay_why, $mailer] = zap_mail_status_line();
    ?>
<div class="wrap" dir="rtl">
  <h1>הגדרות טפסים</h1>
  <?php if ($saved) : ?><div class="notice notice-success"><p>נשמר.</p></div><?php endif; ?>
  <p>כל הטפסים באתר (פוטר, צור קשר, טפסים בעמודים) הם אותו טופס, ושולחים לכתובת שכאן. כל פנייה נשמרת גם ב"פניות מהאתר".</p>
  <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
    <input type="hidden" name="action" value="zap_form_settings">
    <?php wp_nonce_field('zap_form_settings'); ?>
    <table class="form-table" role="presentation">
      <tr><th scope="row"><label for="zfs-to">נמען (המייל של הלקוח)</label></th>
          <td><input id="zfs-to" name="email_leads" type="email" class="regular-text" dir="ltr" value="<?php echo esc_attr(zap_opt('business.email_leads')); ?>"></td></tr>
      <tr><th scope="row">שולח</th>
          <td><code dir="ltr"><?php echo esc_html(zap_mail_from_address()); ?></code> · שם השולח: <?php echo esc_html(zap_opt('business.name', get_bloginfo('name'))); ?>
          <p class="description">השולח הוא כתובת בדומיין של האתר עצמו, כדי ש-SPF/DMARC יאשרו את המייל ולא יסנן אותו לספאם. התשובה (Reply-To) חוזרת לפונה כשהשאיר אימייל.</p></td></tr>
      <tr><th scope="row">מי מנהל את הדואר באתר</th>
          <td><strong><?php echo esc_html($mailer); ?></strong>
          <p class="description"><?php echo esc_html($relay_why); ?></p>
          <p class="description"><?php echo $relay_on
              ? 'ממסר זאפ חל רק על המייל של טופס הפניות. שחזור סיסמה, WooCommerce וכל תוסף אחר נשלחים בדרך הרגילה של האתר.'
              : 'תוסף הדואר שמותקן באתר מנצח תמיד. זאפ לא נוגעת בהגדרות השליחה שלו.'; ?></p></td></tr>
      <tr><th scope="row"><label for="zfs-test">כתובת לבדיקות (אתר בדיקה בלבד)</label></th>
          <td><input id="zfs-test" name="test_to" type="email" class="regular-text" dir="ltr" value="<?php echo esc_attr(zap_opt('smtp.test_to')); ?>">
          <p class="description">באתר בדיקה לא נשלח מייל ללקוח. פניות נשלחות לכתובת הזו אם מולאה.</p></td></tr>
      <tr><th scope="row">מצב</th>
          <td><?php echo $staging ? '<strong>אתר בדיקה:</strong> מיילים ללקוח מושבתים עד העלייה לאוויר.' : '<strong>אתר חי:</strong> כל פנייה נשלחת לנמען.'; ?></td></tr>
    </table>
    <p class="description">הערה: בבנייה מחדש מה-site.json הנמען נלקח משם (business.email_leads). עדכנו גם שם.</p>
    <?php submit_button('שמירה'); ?>
  </form>
</div>
<?php
}

add_action('admin_post_zap_form_settings', function () {
    if (!current_user_can('manage_options')) wp_die('אין הרשאה');
    check_admin_referer('zap_form_settings');
    $o = get_option('zap_site', []);
    $o['business'] = $o['business'] ?? [];
    $o['smtp'] = $o['smtp'] ?? [];
    $o['business']['email_leads'] = sanitize_email(wp_unslash($_POST['email_leads'] ?? ''));
    $o['smtp']['test_to'] = sanitize_email(wp_unslash($_POST['test_to'] ?? ''));
    update_option('zap_site', $o);
    wp_safe_redirect(add_query_arg(['post_type' => 'zap_lead', 'page' => 'zap-form-settings', 'saved' => 1], admin_url('edit.php')));
    exit;
});
