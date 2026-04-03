export const getRiskColor = (score) => {
  if (score <= 33) return 'var(--green)';
  if (score <= 66) return 'var(--amber)';
  return 'var(--red)';
};

export const getConfidenceColor = (score) => {
  if (score > 85) return 'var(--green)';
  if (score > 70) return 'var(--amber)';
  return 'var(--red)';
};

export const getStatusColors = (status) => {
  switch (status) {
    case 'match': return { bg: 'var(--green-dim)', color: 'var(--green)', label: 'Match' };
    case 'quantity_mismatch': return { bg: 'var(--amber-dim)', color: 'var(--amber)', label: 'Qty diff' };
    case 'price_mismatch': return { bg: 'var(--amber-dim)', color: 'var(--amber)', label: 'Price diff' };
    case 'missing_in_po': return { bg: 'var(--red-dim)', color: 'var(--red)', label: 'Not in PO' };
    case 'extra_in_po': return { bg: 'var(--blue-dim)', color: 'var(--blue)', label: 'Extra in PO' };
    case 'extra_in_invoice': return { bg: 'var(--red-dim)', color: 'var(--red)', label: 'Extra in inv' };
    default: return { bg: 'var(--bg-3)', color: 'var(--text-2)', label: status || '—' };
  }
};
