import React from 'react';
import { ShieldCheck, UserCircle, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

const Header = () => {
  return (
    <motion.header 
      className="app-header"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <div className="header-title-wrapper">
        <div className="header-icon">
          <ShieldCheck size={32} />
        </div>
        <div>
          <h1>Validation Hub</h1>
          <p className="subtitle">Invoice vs PO Automated Analysis</p>
        </div>
      </div>
      <div style={{ display: 'flex', gap: '16px', color: 'var(--text-secondary)' }}>
        <button className="btn-view" style={{ border: 'none', background: 'transparent', padding: '8px', boxShadow: 'none' }}>
          <Bell size={22} />
        </button>
        <button className="btn-view" style={{ border: 'none', background: 'transparent', padding: '8px', boxShadow: 'none' }}>
          <UserCircle size={22} />
        </button>
      </div>
    </motion.header>
  );
};

export default Header;
