import React from 'react';
import './CompareSection.css';

const CompareSection = ({ onCompare, disabled, isLoading }) => {
    return (
        <div className="compare-section">
            <button
                className="compare-btn"
                onClick={onCompare}
                disabled={disabled || isLoading}
            >
                {isLoading ? (
                    <span className="loader">Comparing...</span>
                ) : (
                    "Compare Documents"
                )}
            </button>
        </div>
    );
};

export default CompareSection;
