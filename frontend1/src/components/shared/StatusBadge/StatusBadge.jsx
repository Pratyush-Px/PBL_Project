import React from 'react';
import { getStatusColors } from '../../../utils/colors';
import styles from './StatusBadge.module.css';

const StatusBadge = ({ status }) => {
  const { bg, color, label } = getStatusColors(status);
  return (
    <span className={styles.badge} style={{ backgroundColor: bg, color }}>
      {label}
    </span>
  );
};
export default StatusBadge;
