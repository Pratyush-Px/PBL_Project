import React from 'react';
import MetricCard from '../shared/MetricCard/MetricCard';
import { formatCurrency } from '../../utils/formatters';
import styles from './MetricsGrid.module.css';

const MetricsGrid = ({ invoiceTotal, poTotal, difference, lineItemsCount }) => {
  return (
    <div className={styles.gridContainer} style={{ padding: '0 var(--space-12)' }}>
      <MetricCard 
        label="Invoice Total" 
        valueText={`$${formatCurrency(invoiceTotal)}`} 
        countTo={invoiceTotal}
        subLabel="Total amount on invoice" 
        delayMs={80} 
      />
      <MetricCard 
        label="PO Total" 
        valueText={`$${formatCurrency(poTotal)}`} 
        countTo={poTotal}
        subLabel="Total amount on purchase order" 
        delayMs={140} 
      />
      <MetricCard 
        label="Difference" 
        valueText={difference === 0 ? "±0.00" : (difference > 0 ? `+${formatCurrency(difference)}` : `-${formatCurrency(Math.abs(difference))}`)} 
        countTo={Math.abs(difference)}
        valueColor={difference === 0 ? 'var(--green)' : 'var(--red)'}
        subLabel="Amount discrepancy" 
        delayMs={200} 
      />
      <MetricCard 
        label="Line Items" 
        valueText={`${lineItemsCount}`} 
        countTo={lineItemsCount}
        valueColor="var(--blue)"
        subLabel="Total items analyzed" 
        delayMs={260} 
      />
    </div>
  );
};

export default MetricsGrid;
