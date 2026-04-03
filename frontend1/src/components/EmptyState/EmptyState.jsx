import React from 'react';
import styles from './EmptyState.module.css';

const EmptyState = ({ visible }) => {
  return (
    <div className={`${styles.container} ${visible ? styles.visible : styles.hidden}`}>
      <div className={styles.iconContainer}>
        {/* SVG Illustration: two overlapping documents with a checkmark/x */}
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="20" y="24" width="32" height="42" rx="4" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/>
          <path d="M28 16H42.5C44.7091 16 46.5 17.7909 46.5 20V24" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M52 32H60V56C60 58.2091 58.2091 60 56 60H52" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <circle cx="56" cy="24" r="10" stroke="currentColor" strokeWidth="2" fill="var(--bg-0)"/>
          <path d="M52 24L55 27L60 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
      <h2 className={styles.heading}>Select a result</h2>
      <p className={styles.subtext}>
        Choose an audit result from the sidebar to view the full analysis.
      </p>
    </div>
  );
};
export default EmptyState;
