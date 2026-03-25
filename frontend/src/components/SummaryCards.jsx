import React, { useEffect, useState } from 'react';
import { FileText, CheckCircle, XCircle, AlertTriangle, Target } from 'lucide-react';
import { motion, useAnimation } from 'framer-motion';

// Quick Animated Counter Component
const AnimatedNumber = ({ value }) => {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = parseInt(value, 10) || 0;
    if (start === end) {
      setDisplayValue(end);
      return;
    }
    let totalDuration = 1000;
    let incrementTime = (totalDuration / end);
    let timer = setInterval(() => {
      start += 1;
      setDisplayValue(start);
      if (start === end) clearInterval(timer);
    }, incrementTime > 10 ? incrementTime : 10);
    
    return () => clearInterval(timer);
  }, [value]);

  return <>{typeof value === 'number' ? displayValue : value}</>;
};

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

const SummaryCards = ({ results }) => {
  const total = results.length;
  const matches = results.filter(r => (r.match_status || '').toLowerCase() === 'match').length;
  const mismatches = total - matches;
  
  const avgRisk = total > 0 
    ? Math.round(results.reduce((acc, r) => acc + (r.risk_score || 0), 0) / total) 
    : 0;
    
  const resultsWithConf = results.filter(r => r.confidence_score != null);
  const avgConf = resultsWithConf.length > 0
    ? Math.round(resultsWithConf.reduce((acc, r) => acc + r.confidence_score, 0) / resultsWithConf.length)
    : 0;

  return (
    <motion.div 
      className="summary-container"
      variants={containerVariants}
      initial="hidden"
      animate="show"
    >
      <motion.div variants={itemVariants} className="card-premium summary-card-inner">
        <div className="card-icon-wrapper" style={{ background: 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)', color: '#4f46e5' }}>
          <FileText size={24} />
        </div>
        <div className="card-value"><AnimatedNumber value={total} /></div>
        <div className="card-label">Total Validations</div>
      </motion.div>

      <motion.div variants={itemVariants} className="card-premium summary-card-inner">
        <div className="card-icon-wrapper" style={{ background: 'linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)', color: '#15803d' }}>
          <CheckCircle size={24} />
        </div>
        <div className="card-value"><AnimatedNumber value={matches} /></div>
        <div className="card-label">Perfect Matches</div>
      </motion.div>

      <motion.div variants={itemVariants} className="card-premium summary-card-inner">
        <div className="card-icon-wrapper" style={{ background: 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)', color: '#b91c1c' }}>
          <XCircle size={24} />
        </div>
        <div className="card-value" style={{color: mismatches > 0 ? '#b91c1c' : 'inherit'}}>
          <AnimatedNumber value={mismatches} />
        </div>
        <div className="card-label">Mismatches Detected</div>
      </motion.div>

      <motion.div variants={itemVariants} className="card-premium summary-card-inner">
        <div className="card-icon-wrapper" style={{ background: 'linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%)', color: '#c2410c' }}>
          <AlertTriangle size={24} />
        </div>
        <div className="card-value">
          <AnimatedNumber value={avgRisk} /><span style={{fontSize: '1.25rem', color: 'var(--text-muted)'}}>/100</span>
        </div>
        <div className="card-label">System Avg Risk</div>
      </motion.div>

      <motion.div variants={itemVariants} className="card-premium summary-card-inner">
        <div className="card-icon-wrapper" style={{ background: 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)', color: '#4f46e5' }}>
          <Target size={24} />
        </div>
        <div className="card-value"><AnimatedNumber value={avgConf} />%</div>
        <div className="card-label">AI Confidence</div>
      </motion.div>
    </motion.div>
  );
};

export default SummaryCards;
