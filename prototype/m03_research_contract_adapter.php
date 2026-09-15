<?php

declare(strict_types=1);

require_once __DIR__ . '/m03_fixture_renderer.php';

/**
 * Adapt the legacy M03 WordPress fixture into the research-lineage presentation
 * contract without upgrading fixture evidence into live commercial authority.
 */
function mpd_adapt_fixture_to_research_contract(array $fixture): array
{
    mpd_validate_fixture($fixture);

    $freshness = match ($fixture['evidence_state']) {
        'CURRENT' => 'FIXTURE',
        'STALE' => 'STALE',
        default => 'UNKNOWN',
    };

    // Fixture ELIGIBLE is deliberately not equivalent to live VERIFIED Prime.
    $primeState = match ($fixture['evidence_state']) {
        'STALE' => 'STALE',
        default => 'UNKNOWN',
    };

    return [
        'product_id' => $fixture['product_id'],
        'asin' => null,
        'marketplace' => 'UNKNOWN',
        'category_id' => $fixture['category_slug'],
        'title' => $fixture['title'],
        'summary' => '',
        'prime_state' => $primeState,
        'prime_evidence_source' => $fixture['prime_evidence_source'],
        'prime_checked_at' => $fixture['prime_checked_at'],
        'ranking_position' => $fixture['ranking_position'],
        'ranking_method_id' => 'FIXTURE_EDITORIAL_ORDER',
        'ranking_evidence_source' => 'FIXTURE',
        'ranking_checked_at' => $fixture['ranking_checked_at'],
        'product_data_refreshed_at' => $fixture['product_refreshed_at'],
        'evidence_status' => 'FIXTURE',
        'freshness_state' => $freshness,
        'outbound_destination_state' => 'DISABLED',
        'outbound_url' => null,
    ];
}
