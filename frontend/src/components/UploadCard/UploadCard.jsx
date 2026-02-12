import React, { useRef, useState } from 'react';
import './UploadCard.css';

const UploadCard = ({ title, file, onFileSelect, onRemoveFile }) => {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            onFileSelect(droppedFile);
        }
    };

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            onFileSelect(selectedFile);
        }
    };

    return (
        <div className="upload-card">
            <h3>{title}</h3>
            <div
                className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={!file ? handleClick : undefined}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />

                {file ? (
                    <div className="file-info">
                        <div className="file-icon">📄</div>
                        <p className="file-name">{file.name}</p>
                        <button
                            className="remove-btn"
                            onClick={(e) => {
                                e.stopPropagation();
                                onRemoveFile();
                            }}
                        >
                            ×
                        </button>
                    </div>
                ) : (
                    <div className="placeholder">
                        <span className="upload-icon">☁️</span>
                        <p>Drag & Drop or Click to Upload</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadCard;
