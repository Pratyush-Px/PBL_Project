export const formatCurrency = (amount) => {
  if (amount == null) return "—";
  return new Intl.NumberFormat('en-US', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(Math.abs(amount));
};

export const formatDelta = (amount) => {
  if (amount == null) return "—";
  const formatted = formatCurrency(amount);
  if (amount === 0) return `±0.00`;
  if (amount > 0) return `+${formatted}`;
  return `-${formatted}`;
};

export const formatDate = (dateString) => {
  if (!dateString) return "—";
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  }).format(date);
};

export const formatMs = (ms) => {
  if (ms == null) return "—";
  return `${ms}`;
};

export const formatPercent = (value) => {
  if (value == null) return "—";
  return `${value}`;
};
