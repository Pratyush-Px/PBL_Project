import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ResultsTable = ({ results, onView }) => {
  const [filter, setFilter] = useState('all');
  const [sortField, setSortField] = useState('created_at');
  const [sortDir, setSortDir] = useState('desc');

  const filteredAndSorted = useMemo(() => {
    let final = [...results];

    if (filter === 'mismatch') {
      final = final.filter(r => (r.match_status || '').toLowerCase() !== 'match');
    } else if (filter === 'high-risk') {
      final = final.filter(r => r.risk_score > 70);
    }

    final.sort((a, b) => {
      let valA, valB;
      if (sortField === 'risk_score') {
        valA = a.risk_score || 0;
        valB = b.risk_score || 0;
      } else {
        valA = new Date(a.created_at || 0).getTime();
        valB = new Date(b.created_at || 0).getTime();
      }
      if (valA < valB) return sortDir === 'asc' ? -1 : 1;
      if (valA > valB) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });

    return final;
  }, [results, filter, sortField, sortDir]);

  const toggleSort = (field) => {
    if (sortField === field) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDir('desc');
    }
  };

  const getStatusBadge = (status) => {
    const isMatch = (status || '').toLowerCase() === 'match';
    return (
      <span className={`badge ${isMatch ? 'match' : 'mismatch'}`}>
        {isMatch ? 'MATCH' : 'MISMATCH'}
      </span>
    );
  };

  const getRiskBadge = (score) => {
    const s = score || 0;
    const type = s <= 30 ? 'risk-low' : s <= 70 ? 'risk-medium' : 'risk-high';
    return (
      <span className={`badge ${type}`}>
        {s} / 100
      </span>
    );
  };

  const tbodyVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.05 }
    }
  };

  const rowVariants = {
    hidden: { opacity: 0, x: -10 },
    show: { opacity: 1, x: 0, transition: { type: "tween", duration: 0.3 } }
  };

  return (
    <motion.div 
      className="table-card card-premium"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
    >
      <div className="table-header">
        <h3>Validation History</h3>
        <div className="table-controls">
          <select 
            className="filter-select" 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="all">All Results</option>
            <option value="mismatch">Mismatches Only</option>
            <option value="high-risk">High Risk ({'>'}70)</option>
          </select>
        </div>
      </div>
      
      <div className="table-scroll-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Status</th>
              <th 
                style={{cursor: 'pointer'}} 
                onClick={() => toggleSort('risk_score')}
              >
                Risk Score {sortField === 'risk_score' && (sortDir === 'asc' ? '↑' : '↓')}
              </th>
              <th>Confidence</th>
              <th 
                style={{cursor: 'pointer'}} 
                onClick={() => toggleSort('created_at')}
              >
                Date {sortField === 'created_at' && (sortDir === 'asc' ? '↑' : '↓')}
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <motion.tbody
             variants={tbodyVariants}
             initial="hidden"
             animate="show"
             key={filter + sortField + sortDir} // re-trigger animation on sort/filter
          >
            <AnimatePresence>
              {filteredAndSorted.map(r => (
                <motion.tr 
                  key={r.id}
                  variants={rowVariants}
                  exit={{ opacity: 0 }}
                  layout
                >
                  <td className="order-id">{r.order_id}</td>
                  <td>{getStatusBadge(r.match_status)}</td>
                  <td>{getRiskBadge(r.risk_score)}</td>
                  <td style={{fontWeight: 600}}>
                    {r.confidence_score != null ? `${r.confidence_score}%` : '—'}
                  </td>
                  <td className="timestamp">
                    {r.created_at ? new Date(r.created_at).toLocaleString() : '—'}
                  </td>
                  <td>
                    <motion.button 
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="btn-view" 
                      onClick={() => onView(r.id)}
                    >
                      View Details
                    </motion.button>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
            {filteredAndSorted.length === 0 && (
              <tr>
                <td colSpan="6" style={{textAlign: 'center', padding: '60px', color: 'var(--text-secondary)'}}>
                  No matching results found.
                </td>
              </tr>
            )}
          </motion.tbody>
        </table>
      </div>
    </motion.div>
  );
};

export default ResultsTable;
