<?php

declare(strict_types=1);

require_once __DIR__ . '/../prototype/m03_research_contract_adapter.php';

function assert_same($expected, $actual, string $message): void {
    if ($expected !== $actual) {
        throw new RuntimeException($message . ': expected ' . var_export($expected, true) . ', got ' . var_export($actual, true));
    }
}

$base = [
    'product_id' => 'fixture-001', 'asin' => null, 'marketplace' => 'FIXTURE',
    'category_slug' => 'fixture-category', 'title' => 'Synthetic product', 'outbound_url' => null,
    'prime_state' => 'ELIGIBLE', 'prime_evidence_source' => 'FIXTURE',
    'prime_checked_at' => '2026-09-14T00:00:00Z', 'ranking_position' => 1,
    'ranking_method' => 'FIXTURE_EDITORIAL_ORDER', 'ranking_checked_at' => '2026-09-14T00:00:00Z',
    'product_refreshed_at' => '2026-09-14T00:00:00Z', 'evidence_state' => 'CURRENT',
    'evidence_notes' => 'synthetic only',
];

$current = mpd_adapt_fixture_to_research_contract($base);
assert_same('UNKNOWN', $current['prime_state'], 'fixture ELIGIBLE must not become VERIFIED Prime');
assert_same('FIXTURE', $current['freshness_state'], 'fixture CURRENT must remain fixture freshness');
assert_same('DISABLED', $current['outbound_destination_state'], 'fixture destination must remain disabled');
assert_same(null, $current['outbound_url'], 'adapter must not synthesize outbound URL');
assert_same('UNKNOWN', $current['marketplace'], 'fixture marketplace must not become live marketplace authority');

$staleInput = $base;
$staleInput['evidence_state'] = 'STALE';
$stale = mpd_adapt_fixture_to_research_contract($staleInput);
assert_same('STALE', $stale['prime_state'], 'stale fixture evidence must stay stale');
assert_same('STALE', $stale['freshness_state'], 'stale freshness must stay stale');

$unknownInput = $base;
$unknownInput['evidence_state'] = 'UNKNOWN';
$unknownInput['prime_state'] = 'UNKNOWN';
$unknown = mpd_adapt_fixture_to_research_contract($unknownInput);
assert_same('UNKNOWN', $unknown['prime_state'], 'unknown Prime must stay unknown');
assert_same('UNKNOWN', $unknown['freshness_state'], 'unknown freshness must stay unknown');

$bad = $base;
$bad['outbound_url'] = 'https://www.amazon.com/example';
try {
    mpd_adapt_fixture_to_research_contract($bad);
    throw new RuntimeException('live outbound URL was not rejected');
} catch (InvalidArgumentException $expected) {
    // expected: legacy fixture validator fails closed before adaptation.
}

echo "m03 research contract adapter: PASS\n";
