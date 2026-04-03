import React, { useEffect, useState } from 'react';
import { getConfidenceColor } from '../../utils/colors';

const ConfidenceBar = ({ score }) => {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setWidth(score);
    }, 400); // Wait for section entrance
    
    return () => clearTimeout(timeout);
  }, [score]);

  const color = getConfidenceColor(score);
  
  let label = "Low — manual review required";
  if (score > 85) label = "High confidence";
  else if (score > 70) label = "Moderate — verify manually";

  return (
    <div style={{ width: '100%' }}>
      <div style={{ marginBottom: 'var(--space-5)' }}>
        <span style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 300,
          fontSize: 'var(--text-4xl)',
          color: color,
          letterSpacing: '-0.02em',
          lineHeight: 1
        }}>
          <span style={{ fontFamily: 'var(--font-mono)' }}>{score}</span>
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 'var(--text-xl)', color: 'var(--text-3)' }}>%</span>
        </span>
      </div>
      
      {/* Track */}
      <div style={{
        height: '4px',
        backgroundColor: 'var(--bg-4)',
        borderRadius: '2px',
        width: '100%',
        overflow: 'hidden',
        marginBottom: 'var(--space-2)'
      }}>
        {/* Fill */}
        <div style={{
          height: '100%',
          width: `${width}%`,
          backgroundColor: color,
          transition: 'width 1000ms var(--ease-out)'
        }} />
      </div>
      
      <div style={{
        fontFamily: 'var(--font-ui)',
        fontSize: 'var(--text-sm)',
        color: color
      }}>
        {label}
      </div>
    </div>
  );
};

export default ConfidenceBar;
