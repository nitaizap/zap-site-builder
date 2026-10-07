<?php
/**
 * JSON-LD that Yoast does not produce: the local business, FAQPage (from the same data the
 * page renders, so the counts always match) and Service on service pages.
 * Never aggregateRating: ratings appear only from a real, connected reviews source.
 */
defined('ABSPATH') || exit;

function zap_business_schema() {
    $b = zap_opt('business', []);
    if (empty($b['name'])) return null;
    $id = home_url('/#business');
    $s = [
        '@type' => $b['schema_type'] ?? 'LocalBusiness',
        '@id'   => $id,
        'name'  => $b['name'],
        'url'   => home_url('/'),
    ];
    if (!empty($b['legal_name']))  $s['legalName'] = $b['legal_name'];
    if (!empty($b['phone_e164']))  $s['telephone'] = $b['phone_e164'];
    if (!empty($b['email_public'])) $s['email'] = $b['email_public'];
    if ($logo = get_theme_mod('custom_logo')) {
        $u = wp_get_attachment_image_url($logo, 'full');
        $s['logo'] = $u;
        $s['image'] = $u;
    }
    if (!empty($b['street']) || !empty($b['city'])) {
        $s['address'] = array_filter([
            '@type'           => 'PostalAddress',
            'streetAddress'   => $b['street'] ?? '',
            'addressLocality' => $b['city'] ?? '',
            'postalCode'      => $b['postal_code'] ?? '',
            'addressCountry'  => 'IL',
        ]);
    }
    if (!empty($b['geo']['lat'])) {
        $s['geo'] = ['@type' => 'GeoCoordinates', 'latitude' => $b['geo']['lat'], 'longitude' => $b['geo']['lng']];
    }
    if (!empty($b['opening_hours'])) $s['openingHours'] = array_values((array) $b['opening_hours']);
    if (!empty($b['area_served']))  $s['areaServed'] = array_values((array) $b['area_served']);
    if (!empty($b['founded']))      $s['foundingDate'] = (string) $b['founded'];
    $same = array_values(array_filter([$b['gmb_url'] ?? '', $b['gmb_kgmid_url'] ?? '', $b['facebook'] ?? '', $b['instagram'] ?? '', $b['linkedin'] ?? '', $b['youtube'] ?? '']));
    if ($same) $s['sameAs'] = $same;
    if (!empty($b['gmb_url'])) $s['hasMap'] = $b['gmb_url'];
    return $s;
}

add_action('wp_head', function () {
    $graph = [];
    if ($biz = zap_business_schema()) $graph[] = $biz;

    if (is_singular()) {
        $id = get_queried_object_id();
        $faq = json_decode((string) get_post_meta($id, '_zap_faq', true), true);
        if (is_array($faq) && count($faq) > 0) {
            $graph[] = [
                '@type'      => 'FAQPage',
                '@id'        => get_permalink($id) . '#faq',
                'mainEntity' => array_map(fn($x) => [
                    '@type'          => 'Question',
                    'name'           => wp_strip_all_tags($x['q']),
                    'acceptedAnswer' => ['@type' => 'Answer', 'text' => wp_strip_all_tags($x['a'])],
                ], $faq),
            ];
        }
        if (get_post_meta($id, '_zap_page_type', true) === 'service' && $biz) {
            $graph[] = array_filter([
                '@type'       => 'Service',
                '@id'         => get_permalink($id) . '#service',
                'name'        => get_the_title($id),
                'description' => wp_strip_all_tags(get_the_excerpt($id)),
                'provider'    => ['@id' => $biz['@id']],
                'areaServed'  => $biz['areaServed'] ?? null,
                'url'         => get_permalink($id),
            ]);
        }
    }
    if (!$graph) return;
    echo '<script type="application/ld+json">' . wp_json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "</script>\n";
}, 30);
