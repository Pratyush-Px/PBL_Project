import React, { useEffect, useState } from 'react';
import styles from './MetricCard.module.css';

const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

const MetricCard = ({ label, valueText, subLabel, valueColor, delayMs, countTo }) => {
  const [displayVal, setDisplayVal] = useState(0);

  useEffect(() => {
    if (countTo == null || typeof countTo !== 'number') return;
    let start = null;
    let req;
    const duration = 900;
    
    // Staggered trigger via setTimeout
    let timeoutId = setTimeout(() => {
      const step = (timestamp) => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        const ease = easeOutExpo(progress);
        
        setDisplayVal(countTo * ease);
        
        if (progress < 1) {
          req = window.requestAnimationFrame(step);
        } else {
          setDisplayVal(countTo);
        }
      };
      
      req = window.requestAnimationFrame(step);
    }, delayMs || 0);

    return () => {
      clearTimeout(timeoutId);
      if (req) window.cancelAnimationFrame(req);
    };
  }, [countTo, delayMs]);

  // Format the numerical part
  const formattedCount = countTo != null 
    ? new Intl.NumberFormat('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(displayVal)
    : "";
  
  // Reconstruct valueText if counting
  let finalValueText = valueText;
  if (countTo != null && valueText.includes(countTo.toString())) {
    finalValueText = valueText.replace(countTo.toString(), formattedCount);
  }

  return (
    <div className={styles.card} style={{ animationDelay: `${delayMs}ms` }}>
      <div className={styles.label}>{label}</div>
      <div className={styles.value} style={{ color: valueColor || 'var(--text-1)' }}>
        {countTo != null ? finalValueText : valueText}
      </div>
      <div className={styles.sub}>{subLabel}</div>
    </div>
  );
};

export default MetricCard;
