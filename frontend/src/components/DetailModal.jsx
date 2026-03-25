import React, { useEffect } from 'react';
import { X, Clock, ShieldAlert, Cpu, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';
import DetailCharts from './DetailCharts';

const backdropVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.3 } }
};

const modalVariants = {
  hidden: { x: '100%', opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { type: 'spring', damping: 25, stiffness: 200 } },
  exit: { x: '100%', opacity: 0, transition: { duration: 0.3 } }
};

const DetailModal = ({ selectedResult, onClose }) => {
  // Lock body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = 'unset'; }
  }, []);

  if (!selectedResult) return null;

  const getStatusClass = (status) => {
    const s = (status || '').toLowerCase();
    return s === 'match' ? 'match' : 'mismatch';
  };

  const getRiskBadgeClass = (score) => {
    if (score <= 30) return 'risk-low';
    if (score <= 70) return 'risk-medium';
    return 'risk-high';
  };

  const summary = selectedResult.result_json?.summary || {};
  const lineItems = selectedResult.result_json?.line_item_analysis || [];

  return (
    <motion.div 
      className="modal-overlay" 
      variants={backdropVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      onClick={onClose}
    >
      <motion.div 
        className="modal-content" 
        variants={modalVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2>Order {selectedResult.order_id} <span style={{opacity: 0.4, fontSize: '1rem', fontWeight: 500}}>Intelligence Report</span></h2>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div className="detail-section">
            <h3><Cpu size={20} color="var(--primary)" /> Executive Summary</h3>
            <div className="info-grid">
              <div className="info-box">
                <div className="info-box-label">Status</div>
                <span className={`badge ${getStatusClass(selectedResult.match_status)}`}>
                  {selectedResult.match_status}
                </span>
              </div>
              <div className="info-box">
                <div className="info-box-label">Risk Profile</div>
                <span className={`badge ${getRiskBadgeClass(selectedResult.risk_score)}`}>
                  Score: {selectedResult.risk_score} / 100
                </span>
              </div>
              <div className="info-box">
                <div className="info-box-label">AI Confidence</div>
                <div className="info-box-value" style={{color: 'var(--primary)'}}>
                  {selectedResult.confidence_score != null ? `${selectedResult.confidence_score}%` : '—'}
                </div>
              </div>
            </div>
          </div>

          <div className="detail-section">
            <h3><ShieldAlert size={20} color="var(--primary)" /> Financial Overview</h3>
            <div className="info-grid" style={{marginBottom: '20px'}}>
              <div className="info-box">
                <div className="info-box-label">Allocated Invoice Total</div>
                <div className="info-box-value">${summary.invoice_total ?? '—'}</div>
              </div>
              <div className="info-box">
                <div className="info-box-label">Original PO Total</div>
                <div className="info-box-value">${summary.po_total ?? '—'}</div>
              </div>
            </div>
            
            {selectedResult.result_json?.risk_reason && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
                style={{
                  background: 'var(--error-bg)',
                  borderLeft: '4px solid var(--error)',
                  padding: '20px',
                  borderRadius: '0 12px 12px 0',
                  marginBottom: '20px',
                  boxShadow: 'var(--shadow-soft)'
                }}
              >
                <h4 style={{color: '#991b1b', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 700}}>IDENTIFIED RISK FACTOR</h4>
                <p style={{color: '#7f1d1d', fontSize: '0.95rem', fontWeight: 500}}>{selectedResult.result_json.risk_reason}</p>
              </motion.div>
            )}
            {selectedResult.result_json?.processing_time_ms != null && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 500 }}>
                <Clock size={16} /> Processed automatically in {Math.round(selectedResult.result_json.processing_time_ms)} ms
              </div>
            )}
          </div>

          {lineItems.length > 0 && (
            <div className="detail-section">
              <h3><BarChart3 size={20} color="var(--primary)" /> Per-Comparison Analytics</h3>
              <DetailCharts lineItems={lineItems} />
            </div>
          )}

          {lineItems.length > 0 && (
            <div className="detail-section">
              <h3>Line Item Deep Dive</h3>
              <div className="line-items-wrapper">
                <table className="line-items-table">
                  <thead>
                    <tr>
                      <th>Description</th>
                      <th style={{textAlign: 'center'}}>Inv Qty</th>
                      <th style={{textAlign: 'center'}}>PO Qty</th>
                      <th style={{textAlign: 'right'}}>Inv Price</th>
                      <th style={{textAlign: 'right'}}>PO Price</th>
                      <th style={{textAlign: 'center'}}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lineItems.map((item, idx) => {
                      const status = (item.status || '').toLowerCase().replace(/_/g, '-');
                      const isMismatch = status !== 'match';
                      return (
                        <tr key={idx} className={isMismatch ? 'tr-mismatch' : ''}>
                          <td style={{fontWeight: 600}}>{item.description}</td>
                          <td style={{textAlign: 'center'}}>{item.invoice_qty ?? '—'}</td>
                          <td style={{textAlign: 'center'}}>{item.po_qty ?? '—'}</td>
                          <td style={{textAlign: 'right'}}>{item.invoice_price != null ? `$${item.invoice_price.toFixed(2)}` : '—'}</td>
                          <td style={{textAlign: 'right'}}>{item.po_price != null ? `$${item.po_price.toFixed(2)}` : '—'}</td>
                          <td style={{textAlign: 'center'}}>
                            <span className={`badge ${isMismatch ? 'mismatch' : 'match'}`} style={{fontSize: '0.65rem', padding: '4px 8px'}}>
                              {(item.status || '').replace(/_/g, ' ')}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default DetailModal;
