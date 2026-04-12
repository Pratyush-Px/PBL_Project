import React, { useState } from 'react';
import './Methodology.css';
import ImageModal from './ImageModal';

const Methodology = () => {
    const [selectedImage, setSelectedImage] = useState(null);

    return (
        <section id="methodology" className="section-container">
            <h2 className="section-title gradient-text">System Methodology</h2>

            <div className="methodology-flow">
                <div className="method-card glass-card">
                    <div className="card-number">01</div>
                    <h3>Data Input & Preprocessing</h3>
                    <p>
                        Accepts scanned invoices and purchase orders in PDF, JPG, or PNG formats.
                        Applies image preprocessing techniques including grayscale conversion, bilateral filtering, and adaptive thresholding to improve OCR accuracy.
                        All files are processed securely in memory without permanent storage.
                    </p>
                    <div className="card-image-container" onClick={() => setSelectedImage(`${import.meta.env.BASE_URL}images/flowchart.png`)}>
                        <img src={`${import.meta.env.BASE_URL}images/flowchart.png`} alt="Process Flowchart" className="card-thumbnail" />
                        <span className="expand-hint">Click to expand</span>
                    </div>
                </div>

                <div className="flow-arrow">→</div>

                <div className="method-card glass-card">
                    <div className="card-number">02</div>
                    <h3>OCR & Structured Extraction</h3>
                    <p>
                        Uses Tesseract OCR (PSM 6) to extract raw text from documents.
                        Implements rule-based parsing with Regular Expressions to identify key fields such as vendor name, invoice date, line items, quantities, and total amounts.
                        Designed as a modular and deterministic extraction pipeline.
                    </p>
                    <div className="card-image-container" onClick={() => setSelectedImage(`${import.meta.env.BASE_URL}images/detailed_system_working.png`)}>
                        <img src={`${import.meta.env.BASE_URL}images/detailed_system_working.png`} alt="System Architecture" className="card-thumbnail" />
                        <span className="expand-hint">Click to expand</span>
                    </div>
                </div>

                <div className="flow-arrow">→</div>

                <div className="method-card glass-card live-card">
                    <div className="card-number">03</div>
                    <h3>Intelligent Validation Engine</h3>
                    <p>
                        Performs cross-document comparison between purchase order and invoice data.
                        Applies fuzzy string matching (Ratcliff/Obershelp algorithm) for vendor and item name similarity.
                        Uses tolerance-based numeric comparison for totals.
                        Generates discrepancy reports and a match confidence score.
                        Provides downloadable CSV validation reports.
                    </p>
                    <a href="https://pbl-projectfrontend.onrender.com" className="demo-btn">VIEW LIVE DEMO</a>
                </div>
            </div>

            <ImageModal
                isOpen={!!selectedImage}
                imageSrc={selectedImage}
                onClose={() => setSelectedImage(null)}
            />
        </section>
    );
};

export default Methodology;
