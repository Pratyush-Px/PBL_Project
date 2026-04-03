import React from 'react';
import Card from '../shared/Card/Card';
import RiskGauge from '../charts/RiskGauge';
import ConfidenceBar from '../charts/ConfidenceBar';
import styles from './RiskAndConfidence.module.css';

const RiskAndConfidence = ({ riskScore, confidenceScore, riskReason }) => {
  const reasons = riskReason ? riskReason.split(';') : [];
  
  return (
    <div className={`${styles.grid} section-reveal`} style={{ animationDelay: '400ms' }}>
      <Card title="Risk Score">
        <div style={{ marginBottom: 'var(--space-6)' }}>
          <RiskGauge score={riskScore} />
        </div>
        <div className={styles.reasonList}>
          {reasons.map((r, i) => (
            <div key={i} className={styles.reasonItem}>
              <span 
                className={styles.dot} 
                style={{ 
                  backgroundColor: riskScore === 0 ? 'var(--green)' : (riskScore <= 66 ? 'var(--amber)' : 'var(--red)')
                }} 
              />
              <span style={{ 
                color: riskScore === 0 ? 'var(--green)' : 'var(--text-2)'
              }}>
                {r}
              </span>
            </div>
          ))}
        </div>
      </Card>
      
      <Card title="Extraction Confidence">
        <ConfidenceBar score={confidenceScore} />
      </Card>
    </div>
  );
};

export default RiskAndConfidence;
