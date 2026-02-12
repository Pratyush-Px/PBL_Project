import React, { useState } from 'react';
import './DocumentViewer.css';

const DocumentViewer = ({ title, data }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOpen = () => setIsOpen(!isOpen);

    const copyToClipboard = (e) => {
        e.stopPropagation();
        navigator.clipboard.writeText(JSON.stringify(data, null, 2));
        alert("Copied to clipboard!");
    };

    return (
        <div className="document-viewer">
            <div className="viewer-header" onClick={toggleOpen}>
                <h4>{title}</h4>
                <div className="viewer-actions">
                    <button className="copy-btn" onClick={copyToClipboard} title="Copy JSON">
                        📋
                    </button>
                    <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
                </div>
            </div>
            {isOpen && (
                <div className="viewer-content">
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default DocumentViewer;
