import React from 'react';
import Card from '../shared/Card/Card';
import StatusBadge from '../shared/StatusBadge/StatusBadge';
import { formatCurrency } from '../../utils/formatters';
import styles from './LineItemsSection.module.css';

const LineItemsSection = ({ items }) => {
  return (
    <div className={`${styles.section} section-reveal`} style={{ animationDelay: '600ms' }}>
      <Card noPadding>
        <div className={styles.headerArea}>
          <h3 className={styles.cardTitle}>Line Items</h3>
        </div>
        
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th className={styles.thLeft}>Description</th>
                <th className={styles.thRight}>Qty (inv)</th>
                <th className={styles.thRight}>Qty (PO)</th>
                <th className={styles.thRight}>Price (inv)</th>
                <th className={styles.thRight}>Price (PO)</th>
                <th className={styles.thCenter}>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan="6" className={styles.emptyCell}>
                    No line items to compare
                  </td>
                </tr>
              ) : (
                items.map((item, idx) => (
                  <tr key={idx} className={styles.tr}>
                    <td className={`${styles.td} ${styles.tdDesc}`}>{item.description}</td>
                    <td className={`${styles.td} ${styles.tdNum}`}>
                      {item.invoice_qty != null && item.invoice_qty !== 0 ? item.invoice_qty : '—'}
                    </td>
                    <td className={`${styles.td} ${styles.tdNum}`}>
                      {item.po_qty != null && item.po_qty !== 0 ? item.po_qty : '—'}
                    </td>
                    <td className={`${styles.td} ${styles.tdNum}`}>
                      {item.invoice_price != null && item.invoice_price !== 0 ? `$${formatCurrency(item.invoice_price)}` : '—'}
                    </td>
                    <td className={`${styles.td} ${styles.tdNum}`}>
                      {item.po_price != null && item.po_price !== 0 ? `$${formatCurrency(item.po_price)}` : '—'}
                    </td>
                    <td className={`${styles.td} ${styles.tdCenter}`}>
                      <StatusBadge status={item.status} />
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default LineItemsSection;
