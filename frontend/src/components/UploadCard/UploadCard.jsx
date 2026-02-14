import React, { useRef, useState, useEffect } from 'react';
import './UploadCard.css';

const UploadCard = ({ title, file, onFileSelect, onRemoveFile }) => {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);
    const [previewUrl, setPreviewUrl] = useState(null);

    // Create and revoke object URL for image preview
    useEffect(() => {
        if (!file) {
            setPreviewUrl(null);
            return;
        }

        let objectUrl;
        if (file.type.startsWith('image/')) {
            objectUrl = URL.createObjectURL(file);
            setPreviewUrl(objectUrl);
        } else {
            setPreviewUrl(null);
        }

        return () => {
            if (objectUrl) URL.revokeObjectURL(objectUrl);
        };
    }, [file]);

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
        if (!file) {
            fileInputRef.current.click();
        }
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            onFileSelect(selectedFile);
        }
    };

    // Determine icon based on file type
    const isPdf = file?.type === 'application/pdf';

    return (
        <div className="upload-card">
            <h3>{title}</h3>
            <div
                className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleClick}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    accept="image/*,application/pdf"
                />

                {file ? (
                    <div className="file-info">
                        <button
                            className="remove-btn"
                            onClick={(e) => {
                                e.stopPropagation();
                                onRemoveFile();
                            }}
                            title="Remove file"
                        >
                            ×
                        </button>

                        {previewUrl ? (
                            <img src={previewUrl} alt="Preview" className="preview-image" />
                        ) : (
                            <div className="file-icon">
                                {isPdf ? '📄' : '📁'}
                            </div>
                        )}

                        <p className="file-name">{file.name}</p>
                    </div>
                ) : (
                    <div className="placeholder">
                        <span className="upload-icon">☁️</span>
                        <p><strong>Click to upload</strong> or drag and drop</p>
                        <p className="upload-hint">PDF or Images (MAX. 10MB)</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadCard;
