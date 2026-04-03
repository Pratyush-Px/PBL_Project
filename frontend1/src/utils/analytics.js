/**
 * Analytics utility functions for computing chart data from results.
 * All functions safely handle missing/empty data via optional chaining and defaults.
 */

/**
 * Group results by date and return an array of { date, comparisons, avgRisk }.
 */
export function groupByDate(results) {
  if (!results || results.length === 0) return [];

  const map = {};
  const sorted = [...results].sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  sorted.forEach(r => {
    if (!r.created_at) return;
    const dateStr = new Date(r.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
    if (!map[dateStr]) {
      map[dateStr] = { date: dateStr, comparisons: 0, totalRisk: 0 };
    }
    map[dateStr].comparisons++;
    map[dateStr].totalRisk += (r.risk_score || 0);
  });

  return Object.values(map).map(item => ({
    date: item.date,
    comparisons: item.comparisons,
    avgRisk: Math.round(item.totalRisk / item.comparisons),
  }));
}

/**
 * Count matches vs mismatches.
 */
export function countMatches(results) {
  if (!results || results.length === 0) return { match: 0, mismatch: 0 };

  let match = 0;
  let mismatch = 0;
  results.forEach(r => {
    if ((r.match_status || '').toLowerCase() === 'match') match++;
    else mismatch++;
  });
  return { match, mismatch };
}

/**
 * Group results into risk buckets: Low (0-30), Medium (31-70), High (71-100).
 */
export function calculateRiskBuckets(results) {
  if (!results || results.length === 0) return { low: 0, medium: 0, high: 0 };

  let low = 0, medium = 0, high = 0;
  results.forEach(r => {
    const s = r.risk_score ?? 0;
    if (s <= 30) low++;
    else if (s <= 70) medium++;
    else high++;
  });
  return { low, medium, high };
}

/**
 * Count high risk vs low risk items (threshold: 70).
 */
export function countHighVsLowRisk(results) {
  if (!results || results.length === 0) return [];

  let high = 0;
  let low = 0;
  results.forEach(r => {
    if ((r.risk_score ?? 0) > 70) high++;
    else low++;
  });
  return [
    { name: 'High Risk (>70)', value: high, color: '#ef4444' },
    { name: 'Normal (≤70)', value: low, color: '#22c55e' },
  ];
}

// ──────────────────────────────────────────────
// Detail-level analytics (single comparison)
// ──────────────────────────────────────────────

/**
 * From result_json.line_item_analysis, count matched vs mismatched line items.
 */
export function countLineItemMatches(lineItems) {
  if (!lineItems || lineItems.length === 0) return [];

  let matched = 0;
  let mismatched = 0;
  lineItems.forEach(item => {
    const s = (item.status || '').toLowerCase();
    if (s === 'match') matched++;
    else mismatched++;
  });
  return [
    { name: 'Matched', value: matched, color: '#22c55e' },
    { name: 'Mismatched', value: mismatched, color: '#ef4444' },
  ];
}

/**
 * Extract mismatch types from line items and count by category.
 * Categories are derived from the status field (e.g., quantity_mismatch, price_mismatch, missing_in_po, etc.).
 */
export function extractMismatchTypes(lineItems) {
  if (!lineItems || lineItems.length === 0) return [];

  const typeMap = {};
  lineItems.forEach(item => {
    const s = (item.status || '').toLowerCase();
    if (s === 'match') return; // skip matches

    // Normalize the status string into a readable category name
    const category = s.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    typeMap[category] = (typeMap[category] || 0) + 1;
  });

  const colors = ['#ef4444', '#f59e0b', '#8b5cf6', '#3b82f6', '#ec4899', '#14b8a6'];
  return Object.entries(typeMap).map(([name, count], i) => ({
    name,
    count,
    fill: colors[i % colors.length],
  }));
}

/**
 * Build field-level comparison data: invoice value vs PO value for each line item.
 * Uses the price field for a meaningful numerical comparison.
 */
export function buildFieldComparison(lineItems) {
  if (!lineItems || lineItems.length === 0) return [];

  return lineItems
    .filter(item => item.invoice_price != null || item.po_price != null)
    .map(item => ({
      name: (item.description || 'Unknown').substring(0, 20),
      invoice: item.invoice_price ?? 0,
      po: item.po_price ?? 0,
    }));
}
