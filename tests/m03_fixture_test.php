<?php

declare(strict_types=1);

require __DIR__ . '/../prototype/m03_fixture_renderer.php';

function check(bool $condition, string $message): void
{
    if (!$condition) {
        throw new RuntimeException($message);
    }
}

function expect_invalid(array $product, string $message): void
{
    try {
        mpd_validate_fixture($product);
    } catch (InvalidArgumentException $e) {
        return;
    }
    throw new RuntimeException($message);
}

$fixtures = json_decode((string)file_get_contents(__DIR__ . '/../fixtures/m03-products.json'), true, flags: JSON_THROW_ON_ERROR);
check(count($fixtures) === 3, 'expected exactly three synthetic products');

$html = mpd_render_fixture_category(array_reverse($fixtures));
check(strpos($html, 'SYNTH-001') < strpos($html, 'SYNTH-002') && strpos($html, 'SYNTH-002') < strpos($html, 'SYNTH-003'), 'fixture ranking order must be deterministic');
check(str_contains($html, 'Evidence: CURRENT') && str_contains($html, '2026-09-14T00:00:00Z'), 'CURRENT evidence must render status and timestamp');
check(str_contains($html, 'Evidence: STALE — verification expired'), 'STALE evidence must be visibly stale');

$unknownHtml = mpd_render_fixture($fixtures[2]);
check(str_contains($unknownHtml, 'UNKNOWN / UNVERIFIED'), 'UNKNOWN evidence must be explicit');
check(!str_contains($unknownHtml, 'Fixture Prime state: ELIGIBLE'), 'UNKNOWN evidence must not infer Prime eligibility');
check(!str_contains($unknownHtml, 'Fixture rank:'), 'UNKNOWN evidence must not render positive ranking claim');
check(!str_contains($html, '<a ') && !str_contains($html, 'amazon.'), 'null outbound URL must produce no Amazon/affiliate CTA');
check(substr_count($html, 'NON-PRODUCTION FIXTURE') === 3, 'every product must carry fixture marker');

$staled = $fixtures[0];
$identity = $staled['product_id'];
$staled['evidence_state'] = 'STALE';
$staleHtml = mpd_render_fixture($staled);
check($staled['product_id'] === $identity && str_contains($staleHtml, 'Evidence: STALE'), 'CURRENT to STALE must preserve canonical fixture identity');

$badState = $fixtures[0];
$badState['evidence_state'] = 'FRESHISH';
expect_invalid($badState, 'unsupported evidence state must fail closed');

$missingCurrentEvidence = $fixtures[0];
$missingCurrentEvidence['prime_checked_at'] = null;
expect_invalid($missingCurrentEvidence, 'CURRENT missing evidence timestamp must fail closed');

$unknownPositive = $fixtures[2];
$unknownPositive['prime_state'] = 'ELIGIBLE';
expect_invalid($unknownPositive, 'UNKNOWN evidence cannot assert Prime eligibility');

$liveIdentifier = $fixtures[0];
$liveIdentifier['asin'] = 'B000REAL123';
expect_invalid($liveIdentifier, 'live ASIN must be forbidden in synthetic fixture');

$providerSpecific = $fixtures[0];
$providerSpecific['ranking_method'] = 'PA_API_RANK';
expect_invalid($providerSpecific, 'provider-specific ranking method must be rejected');

$encoded = json_encode($fixtures, JSON_THROW_ON_ERROR);
foreach (['price', 'stock', 'affiliate_url', 'credential', 'customer_data', 'payment'] as $forbidden) {
    check(!str_contains($encoded, '"' . $forbidden . '"'), "forbidden commercial/live field present: {$forbidden}");
}

echo "PASS: 13 deterministic M-03 fixture checks\n";
