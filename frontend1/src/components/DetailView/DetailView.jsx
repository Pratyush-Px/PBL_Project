import React, { useEffect, useState } from 'react';
import { useResultDetail } from '../../hooks/useResultDetail';
import { useResults } from '../../hooks/useResults';
import HeroSection from '../sections/HeroSection';
import MetricsGrid from '../sections/MetricsGrid';
import AmountComparison from '../sections/AmountComparison';
import RiskAndConfidence from '../sections/RiskAndConfidence';
import StatusBreakdown from '../sections/StatusBreakdown';
import RiskHistory from '../sections/RiskHistory';
import LineItemsSection from '../sections/LineItemsSection';
import styles from './DetailView.module.css';

const DetailContent = ({ selectedId }) => {
  const { detail, loading } = useResultDetail(selectedId);
  const { results } = useResults();

  if (loading || !detail) {
    return null; 
  }

  const { result_json: r, order_id, created_at, match_status } = detail;
  const summary = r.summary;

  return (
    <div className={styles.scrollArea}>
      <div className={styles.innerStack}>
        <HeroSection 
          orderId={order_id} 
          status={match_status} 
          date={created_at} 
          ms={r.processing_time_ms} 
          difference={summary.difference} 
        />
        
        <MetricsGrid 
          invoiceTotal={summary.invoice_total} 
          poTotal={summary.po_total} 
          difference={summary.difference} 
          lineItemsCount={r.line_item_analysis?.length || 0} 
        />
        
        <AmountComparison 
          invoiceTotal={summary.invoice_total} 
          poTotal={summary.po_total} 
        />
        
        <RiskAndConfidence 
          riskScore={r.risk_score} 
          confidenceScore={r.confidence_score} 
          riskReason={r.risk_reason} 
        />
        
        <StatusBreakdown 
          lineItems={r.line_item_analysis || []} 
        />
        
        <RiskHistory 
          allResults={results} 
          selectedOrderId={order_id} 
        />
        
        <LineItemsSection 
          items={r.line_item_analysis || []} 
        />
      </div>
    </div>
  );
};

const DetailView = ({ selectedId }) => {
  const [activeId, setActiveId] = useState(selectedId);
  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    if (selectedId !== activeId && selectedId) {
      if (!activeId) {
        // First selection, no fade out
        setActiveId(selectedId);
      } else {
        setIsFadingOut(true);
        const timer = setTimeout(() => {
          setActiveId(selectedId);
          setIsFadingOut(false);
        }, 150); // 150ms fade out before swapping
        return () => clearTimeout(timer);
      }
    } else if (!selectedId) {
       // Clear selection case
       setIsFadingOut(true);
       const timer = setTimeout(() => {
         setActiveId(null);
         setIsFadingOut(false);
       }, 150);
       return () => clearTimeout(timer);
    }
  }, [selectedId, activeId]);

  if (!activeId) return null;

  return (
    <div className={`${styles.detailViewWrapper} ${isFadingOut ? styles.fadeOut : styles.fadeIn}`}>
      {/* Remount entirely on ID change so animations reset natively */}
      <DetailContent key={activeId} selectedId={activeId} />
    </div>
  );
};

export default DetailView;
