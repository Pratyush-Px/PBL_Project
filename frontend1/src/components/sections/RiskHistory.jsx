import React from 'react';
import Card from '../shared/Card/Card';
import RiskAreaChart from '../charts/RiskAreaChart';
import styles from './RiskHistory.module.css';

const RiskHistory = ({ allResults, selectedOrderId }) => {
  // Sort and prep data
  const data = [...allResults]
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    .map(res => ({
      shortId: res.order_id,
      orderId: res.order_id,
      score: res.risk_score
    }));

  return (
    <div className={`${styles.section} section-reveal`} style={{ animationDelay: '540ms' }}>
      <Card 
        title="Risk History"
        subtitle="Risk scores across all audited orders"
      >
        <RiskAreaChart data={data} selectedOrderId={selectedOrderId} />
      </Card>
    </div>
  );
};

export default RiskHistory;
