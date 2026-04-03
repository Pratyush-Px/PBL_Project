import React from 'react';
import { AlertTriangle, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

const AlertsPanel = ({ results, onView }) => {
  const topRisks = [...results]
    .filter(r => r.risk_score > 30) 
    .sort((a, b) => (b.risk_score || 0) - (a.risk_score || 0))
    .slice(0, 5);

  if (topRisks.length === 0) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, x: 30 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="alerts-card card-premium"
    >
      <div className="alerts-header">
        <AlertTriangle size={24} />
        <h3>Action Needed: High Risk</h3>
      </div>
      <div className="alerts-list">
        {topRisks.map((r, i) => (
          <motion.div 
            key={r.id} 
            className="alert-item"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 + 0.3 }}
            onClick={() => onView(r.id)}
          >
            <div className="alert-info">
              <span className="alert-id">Order {r.order_id}</span>
              <span className="alert-score">
                Risk Factor: {r.risk_score}/100
              </span>
            </div>
            <div style={{ color: '#c2410c', opacity: 0.6 }}>
              <ChevronRight size={20} />
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default AlertsPanel;
