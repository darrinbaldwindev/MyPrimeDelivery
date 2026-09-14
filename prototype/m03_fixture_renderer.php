<?php

declare(strict_types=1);

function mpd_validate_fixture(array $product): void
{
    $required = [
        'product_id', 'asin', 'marketplace', 'category_slug', 'title', 'outbound_url',
        'prime_state', 'prime_evidence_source', 'prime_checked_at', 'ranking_position',
        'ranking_method', 'ranking_checked_at', 'product_refreshed_at', 'evidence_state',
        'evidence_notes'
    ];

    foreach ($required as $field) {
        if (!array_key_exists($field, $product)) {
            throw new InvalidArgumentException("missing field: {$field}");
        }
    }

    if ($product['marketplace'] !== 'FIXTURE') {
        throw new InvalidArgumentException('marketplace must be FIXTURE');
    }
    if ($product['asin'] !== null || $product['outbound_url'] !== null) {
        throw new InvalidArgumentException('live identifiers and outbound URLs are forbidden');
    }
    if (!in_array($product['prime_state'], ['ELIGIBLE', 'NOT_ELIGIBLE', 'UNKNOWN'], true)) {
        throw new InvalidArgumentException('unsupported prime_state');
    }
    if (!in_array($product['evidence_state'], ['CURRENT', 'STALE', 'UNKNOWN'], true)) {
        throw new InvalidArgumentException('unsupported evidence_state');
    }
    if ($product['ranking_method'] !== 'FIXTURE_EDITORIAL_ORDER') {
        throw new InvalidArgumentException('unsupported ranking_method');
    }
    if (!is_int($product['ranking_position']) || $product['ranking_position'] < 1) {
        throw new InvalidArgumentException('ranking_position must be positive integer');
    }
    if ($product['evidence_state'] === 'CURRENT') {
        foreach (['prime_evidence_source', 'prime_checked_at', 'ranking_checked_at'] as $field) {
            if (!is_string($product[$field]) || $product[$field] === '') {
                throw new InvalidArgumentException("CURRENT evidence requires {$field}");
            }
        }
    }
    if ($product['evidence_state'] === 'UNKNOWN' && $product['prime_state'] !== 'UNKNOWN') {
        throw new InvalidArgumentException('UNKNOWN evidence cannot assert Prime eligibility');
    }
}

function mpd_render_fixture(array $product): string
{
    mpd_validate_fixture($product);

    $title = htmlspecialchars((string)$product['title'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $id = htmlspecialchars((string)$product['product_id'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $state = $product['evidence_state'];

    $parts = [
        '<article data-fixture="true" data-product-id="' . $id . '">',
        '<strong>NON-PRODUCTION FIXTURE</strong>',
        '<h2>' . $title . '</h2>',
    ];

    if ($state === 'CURRENT') {
        $parts[] = '<p>Evidence: CURRENT</p>';
        $parts[] = '<p>Fixture Prime state: ' . htmlspecialchars((string)$product['prime_state'], ENT_QUOTES, 'UTF-8') . '</p>';
        $parts[] = '<p>Fixture rank: ' . (int)$product['ranking_position'] . '</p>';
        $parts[] = '<p>Checked: ' . htmlspecialchars((string)$product['prime_checked_at'], ENT_QUOTES, 'UTF-8') . '</p>';
    } elseif ($state === 'STALE') {
        $parts[] = '<p>Evidence: STALE — verification expired</p>';
    } else {
        $parts[] = '<p>Evidence: UNKNOWN / UNVERIFIED</p>';
    }

    $parts[] = '</article>';
    return implode("\n", $parts);
}

function mpd_render_fixture_category(array $products): string
{
    foreach ($products as $product) {
        mpd_validate_fixture($product);
    }
    usort($products, static fn(array $a, array $b): int => $a['ranking_position'] <=> $b['ranking_position']);
    return implode("\n", array_map('mpd_render_fixture', $products));
}
