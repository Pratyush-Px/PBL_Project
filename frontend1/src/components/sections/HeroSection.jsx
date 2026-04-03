import React from 'react';
import { formatDelta, formatDate, formatMs } from '../../utils/formatters';

const HeroSection = ({ orderId, status, date, ms, difference }) => {
  const isZero = difference === 0;
  
  // Convert status to human readable headline
  let headline = "Analysis complete";
  if (status === "match") headline = "Invoice matched";
  if (status === "mismatch") headline = "Discrepancy detected";

  return (
    <div 
      className="section-reveal" 
      style={{
        padding: 'var(--space-10) var(--space-12) 0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        animationDelay: '0ms'
      }}
    >
      <div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 'var(--text-xs)',
          color: 'var(--text-3)',
          letterSpacing: '0.08em',
          textTransform: 'uppercase',
          marginBottom: 'var(--space-2)'
        }}>
          Order #{orderId}
        </div>
        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 300,
          fontSize: 'var(--text-3xl)',
          color: 'var(--text-1)',
          lineHeight: 1.1,
          letterSpacing: '-0.02em',
          margin: '0 0 var(--space-2) 0'
        }}>
          {headline}
        </h1>
        <div style={{
          fontFamily: 'var(--font-ui)',
          fontSize: 'var(--text-sm)',
          color: 'var(--text-3)'
        }}>
          Processed {formatDate(date)} · {formatMs(ms)}ms extraction time
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 300,
          fontSize: 'var(--text-3xl)',
          color: isZero ? 'var(--green)' : 'var(--red)',
          lineHeight: 1.1,
          letterSpacing: '-0.02em'
        }}>
          {formatDelta(difference)}
        </div>
        <div style={{
          fontFamily: 'var(--font-ui)',
          fontSize: 'var(--text-xs)',
          color: 'var(--text-3)',
          marginTop: 'var(--space-2)'
        }}>
          invoice vs purchase order delta
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
