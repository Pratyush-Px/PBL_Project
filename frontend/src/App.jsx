import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

import Header from './components/Header';
import SummaryCards from './components/SummaryCards';
import Visualizations from './components/Visualizations';
import AlertsPanel from './components/AlertsPanel';
import ResultsTable from './components/ResultsTable';
import DetailModal from './components/DetailModal';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedResult, setSelectedResult] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const res = await fetch(`/results`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResults(data);
      setError(null);
    } catch (err) {
      setError('Failed to load results. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const viewDetail = async (id) => {
    try {
      setDetailLoading(true);
      const res = await fetch(`/results/${id}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setSelectedResult(data);
    } catch (err) {
      alert('Failed to load details');
    } finally {
      setDetailLoading(false);
    }
  };

  const closeDetail = () => setSelectedResult(null);

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div 
              key="loading"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="loading-wrapper"
            >
              <div className="spinner"></div>
              <p style={{ fontWeight: 500 }}>Initializing Insights Engine...</p>
            </motion.div>
          )}

          {error && (
            <motion.div 
              key="error"
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
              style={{ padding: '24px', background: 'var(--error-bg)', border: '1px solid var(--error)', borderRadius: '12px', color: 'var(--error)' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                 <span style={{ fontSize: '1.5rem' }}>⚠️</span> 
                 <div style={{ flexGrow: 1 }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Connection Failed</h3>
                    <p style={{ margin: 0, fontSize: '0.9rem', opacity: 0.8 }}>{error}</p>
                 </div>
                 <button onClick={fetchResults} className="btn-view" style={{ background: '#fff', color: 'var(--error)' }}>
                   Retry Connection
                 </button>
              </div>
            </motion.div>
          )}

          {!loading && !error && results.length === 0 && (
            <motion.div 
              key="empty"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="loading-wrapper"
            >
              <h2 style={{fontSize: '1.5rem', color: 'var(--text-primary)'}}>No intel gathered yet</h2>
              <p style={{fontSize: '1rem', color: 'var(--text-secondary)'}}>Run document validations via the backend API to populate your dashboard.</p>
            </motion.div>
          )}

          {!loading && results.length > 0 && (
            <motion.div 
              key="content"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}
            >
              <SummaryCards results={results} />
              
              <div className="middle-section">
                <Visualizations results={results} />
                <div>
                  <AlertsPanel results={results} onView={viewDetail} />
                </div>
              </div>

              <ResultsTable results={results} onView={viewDetail} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <AnimatePresence>
        {selectedResult && (
          <DetailModal selectedResult={selectedResult} onClose={closeDetail} />
        )}
      </AnimatePresence>
      
      {/* Small loading overlay for modal fetch */}
      <AnimatePresence>
        {detailLoading && !selectedResult && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            style={{ position: 'fixed', inset: 0, background: 'rgba(255,255,255,0.6)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}
          >
            <div className="spinner"></div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
