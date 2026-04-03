import React, { useEffect, useState } from 'react';
import { getRiskColor } from '../../utils/colors';

const formatGaugePath = (cx, cy, r, startAngle, endAngle) => {
  const polarToCartesian = (cx, cy, r, angleInDegrees) => {
    const angleInRadians = (angleInDegrees - 180) * Math.PI / 180.0;
    return {
      x: cx + (r * Math.cos(angleInRadians)),
      y: cy + (r * Math.sin(angleInRadians))
    };
  };

  const start = polarToCartesian(cx, cy, r, startAngle);
  const end = polarToCartesian(cx, cy, r, endAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

  // M = start, A = rx ry x-axis-rotation large-arc-flag sweep-flag x y
  return [
    "M", start.x, start.y, 
    "A", r, r, 0, largeArcFlag, 1, end.x, end.y
  ].join(" ");
};

const polarToCartesian = (cx, cy, r, angleInDegrees) => {
  const angleInRadians = (angleInDegrees - 180) * Math.PI / 180.0;
  return {
    x: cx + (r * Math.cos(angleInRadians)),
    y: cy + (r * Math.sin(angleInRadians))
  };
};

const RiskGauge = ({ score }) => {
  const cx = 100;
  const cy = 100;
  const r = 80;
  
  const [dotPos, setDotPos] = useState(polarToCartesian(cx, cy, r, 0));
  
  useEffect(() => {
    // Delay animation to align with entrance timing
    const timeout = setTimeout(() => {
      // score 0 = 0 deg (left), score 100 = 180 deg (right)
      const mappedAngle = (score / 100) * 180;
      setDotPos(polarToCartesian(cx, cy, r, mappedAngle));
    }, 400); // 400ms delay to wait for card entrance
    
    return () => clearTimeout(timeout);
  }, [score]);

  const scoreColor = getRiskColor(score);

  return (
    <div style={{ position: 'relative', width: 200, height: 110, margin: '0 auto' }}>
      <svg width="200" height="110" viewBox="0 0 200 110" style={{ overflow: 'visible' }}>
        {/* Background track (optional, instructions say rendered as three colored arcs to form track. We do background too just in case but we will overlay the pieces) */}
        
        {/* Green arc: 0-33% -> 0 to 60 deg */}
        <path 
          d={formatGaugePath(cx, cy, r, 0, 60)} 
          fill="none" 
          stroke="var(--green)" 
          strokeWidth="10" 
          strokeLinecap="round" 
        />
        {/* Amber arc: 33-66% -> 60 to 120 deg (overlap slightly with square caps to connect cleanly, or just keep it tight) */}
        <path 
          d={formatGaugePath(cx, cy, r, 60.5, 119.5)} 
          fill="none" 
          stroke="var(--amber)" 
          strokeWidth="10" 
        />
        {/* Red arc: 66-100% -> 120 to 180 deg */}
        <path 
          d={formatGaugePath(cx, cy, r, 120, 180)} 
          fill="none" 
          stroke="var(--red)" 
          strokeWidth="10" 
          strokeLinecap="round" 
        />

        {/* Animated needle dot */}
        <circle 
          cx={dotPos.x} 
          cy={dotPos.y} 
          r="6" 
          fill="var(--text-1)" 
          style={{ transition: 'cx 800ms var(--ease-spring), cy 800ms var(--ease-spring)' }} 
        />
      </svg>
      
      {/* Center Text overlays */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', textAlign: 'center' }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 300,
          fontSize: '36px',
          color: scoreColor,
          lineHeight: 1,
          letterSpacing: '-0.02em'
        }}>
          {score}
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 'var(--text-xs)',
          color: 'var(--text-3)',
          marginTop: 'var(--space-1)'
        }}>
          / 100
        </div>
      </div>
    </div>
  );
};

export default RiskGauge;
