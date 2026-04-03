import React from 'react';
import styles from './Card.module.css';

const Card = ({ title, subtitle, rightContent, children, style, noPadding }) => {
  return (
    <div className={styles.card} style={style}>
      {(title || rightContent) && (
        <div className={styles.header}>
          <div>
            {title && <h3 className={styles.title}>{title}</h3>}
            {subtitle && <p className={styles.sub}>{subtitle}</p>}
          </div>
          {rightContent && <div className={styles.right}>{rightContent}</div>}
        </div>
      )}
      <div className={noPadding ? "" : styles.content}>
        {children}
      </div>
    </div>
  );
};

export default Card;
