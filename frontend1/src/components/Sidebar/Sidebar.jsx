import React, { useState, useMemo } from 'react';
import { useResults } from '../../hooks/useResults';
import { formatDate } from '../../utils/formatters';
import { getRiskColor } from '../../utils/colors';
import styles from './Sidebar.module.css';

const Sidebar = ({ selectedId, onSelectResult }) => {
  const { results, loading } = useResults();
  const [filterMode, setFilterMode] = useState('all'); // all, match, mismatch
  const [searchQuery, setSearchQuery] = useState('');

  const stats = useMemo(() => {
    let total = results.length;
    let matched = results.filter(r => r.match_status === 'match').length;
    let mismatched = total - matched;
    return { total, matched, mismatched };
  }, [results]);

  const filteredResults = useMemo(() => {
    return results.filter(r => {
      if (filterMode === 'match' && r.match_status !== 'match') return false;
      if (filterMode === 'mismatch' && r.match_status === 'match') return false;
      if (searchQuery && !r.order_id.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      return true;
    });
  }, [results, filterMode, searchQuery]);

  return (
    <aside className={styles.sidebar}>
      {/* Summary strip */}
      <div className={styles.summaryStrip}>
        {stats.total} total <span className={styles.dot}>·</span> {stats.matched} matched <span className={styles.dot}>·</span> {stats.mismatched} mismatched
      </div>

      {/* Filter tabs */}
      <div className={styles.tabsContainer}>
        {['all', 'match', 'mismatch'].map(mode => (
          <button 
            key={mode}
            className={`${styles.tab} ${filterMode === mode ? styles.tabActive : ''}`}
            onClick={() => setFilterMode(mode)}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>

      {/* Search input */}
      <div className={styles.searchContainer}>
        <input 
          className={styles.searchInput}
          placeholder="Search orders..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Section label */}
      <div className={styles.sectionLabel}>RESULTS</div>

      {/* Results List */}
      <div className={styles.list}>
        {loading ? (
          <div className={styles.empty}>Loading...</div>
        ) : filteredResults.length === 0 ? (
          <div className={styles.empty}>No results found</div>
        ) : (
          filteredResults.map((res, index) => {
            const isActive = selectedId === res.id;
            const isMatch = res.match_status === 'match';
            const riskColor = getRiskColor(res.risk_score);
            
            return (
              <div 
                key={res.id}
                onClick={() => onSelectResult(res.id)}
                className={`${styles.resultCard} ${isActive ? styles.active : ''}`}
                style={{ 
                  '--accent-color': isMatch ? 'var(--green)' : 'var(--red)',
                  animationDelay: `${index * 40}ms`
                }}
              >
                <div className={styles.cardContent}>
                  <div className={styles.row1}>
                    <span className={styles.orderId}>{res.order_id}</span>
                    <span 
                      className={styles.miniBadge} 
                      style={{ 
                        backgroundColor: isMatch ? 'var(--green-dim)' : 'var(--red-dim)',
                        color: isMatch ? 'var(--green)' : 'var(--red)'
                      }}
                    >
                      {isMatch ? 'Match' : 'Mismatch'}
                    </span>
                  </div>
                  <div className={styles.row2}>
                    <span className={styles.date}>{formatDate(res.created_at)}</span>
                    <span className={styles.riskScore} style={{ color: riskColor }}>
                      {res.risk_score}
                    </span>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
