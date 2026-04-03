import React from 'react';
import Card from '../shared/Card/Card';
import StatusDonut from '../charts/StatusDonut';
import styles from './StatusBreakdown.module.css';

const StatusBreakdown = ({ lineItems }) => {
  // Aggregate statuses
  const countMap = {};
  lineItems.forEach(item => {
    countMap[item.status] = (countMap[item.status] || 0) + 1;
  });
  
  const data = Object.keys(countMap).map(key => ({
    name: key,
    value: countMap[key]
  }));

  const badgeObj = (
    <span className={styles.badge}>
      {lineItems.length} items
    </span>
  );

  return (
    <div className={`${styles.section} section-reveal`} style={{ animationDelay: '480ms' }}>
      <Card 
        title="Line Item Breakdown"
        rightContent={badgeObj}
      >
        <StatusDonut data={data} />
      </Card>
    </div>
  );
};

export default StatusBreakdown;
