import React from 'react';
import Card from '../shared/Card/Card';
import AmountBarChart from '../charts/AmountBarChart';
import styles from './AmountComparison.module.css';

const AmountComparison = ({ invoiceTotal, poTotal }) => {
  const isMatch = invoiceTotal === poTotal;

  return (
    <div className={`${styles.section} section-reveal`} style={{ animationDelay: '320ms' }}>
      <Card 
        title="Amount Comparison" 
        subtitle="Invoice total vs purchase order total"
      >
        {isMatch && (
          <div className={styles.matchIndicator}>
            Perfect match ✓
          </div>
        )}
        <AmountBarChart invoiceTotal={invoiceTotal} poTotal={poTotal} />
      </Card>
    </div>
  );
};

export default AmountComparison;
