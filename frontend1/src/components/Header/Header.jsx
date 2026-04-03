import React, { useState } from 'react';
import { useApi } from '../../context/ApiContext';
import { useResults } from '../../hooks/useResults';
import styles from './Header.module.css';

const Header = () => {
  const { baseUrl, setBaseUrl, handleSync } = useApi();
  const { isMockMode } = useResults();
  
  const [urlInput, setUrlInput] = useState(baseUrl);

  const onSync = () => {
    setBaseUrl(urlInput);
    handleSync();
  };

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <svg 
          viewBox="0 0 24 24" 
          width="20" height="20" 
          fill="none" stroke="var(--text-1)" 
          strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
        >
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
        <span className={styles.wordmark}>Auditly</span>
      </div>
      
      <div className={styles.right}>
        <input 
          className={styles.input} 
          value={urlInput}
          onChange={(e) => setUrlInput(e.target.value)}
          placeholder="API URL"
        />
        <button className={styles.syncBtn} onClick={onSync}>
          Sync
        </button>
        
        {isMockMode ? (
          <div className={`${styles.pill} ${styles.pillDemo}`}>
            ◌ Demo
          </div>
        ) : (
          <div className={`${styles.pill} ${styles.pillLive}`}>
            ● Live
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
