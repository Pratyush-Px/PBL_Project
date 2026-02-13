import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import UploadCard from './components/UploadCard/UploadCard';
import CompareSection from './components/CompareSection/CompareSection';
import ResultsSection from './components/ResultsSection/ResultsSection';
import { compareDocuments } from './api/api';
import './App.css';

function App() {
  const [orderFile, setOrderFile] = useState(null);
  const [invoiceFile, setInvoiceFile] = useState(null);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCompare = async () => {
    if (!orderFile || !invoiceFile) {
      setError("Please upload both Purchase Order and Invoice files.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setComparisonResult(null);

    try {
      const data = await compareDocuments(orderFile, invoiceFile);
      setComparisonResult(data);
    } catch (err) {
      setError(err.message || "An error occurred during comparison.");
    } finally {
      setIsLoading(false);
    }
  };

  const clearError = () => setError(null);

  return (
    <>
      <Navbar />
      <div className="app-container">

        {error && (
          <div className="error-message">
            Error: {error}
            <button onClick={clearError} style={{ marginLeft: '10px', all: 'unset', cursor: 'pointer', fontWeight: 'bold' }}>✕</button>
          </div>
        )}

        <div className="upload-section">
          <UploadCard
            title="Upload Purchase Order"
            file={orderFile}
            onFileSelect={(file) => { setOrderFile(file); setComparisonResult(null); }}
            onRemoveFile={() => { setOrderFile(null); setComparisonResult(null); }}
          />
          <UploadCard
            title="Upload Invoice"
            file={invoiceFile}
            onFileSelect={(file) => { setInvoiceFile(file); setComparisonResult(null); }}
            onRemoveFile={() => { setInvoiceFile(null); setComparisonResult(null); }}
          />
        </div>

        <CompareSection
          onCompare={handleCompare}
          disabled={!orderFile || !invoiceFile}
          isLoading={isLoading}
        />

        {isLoading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>AI analyzing documents...</p>
          </div>
        )}

        {comparisonResult && !isLoading && (
          <ResultsSection result={comparisonResult} />
        )}

      </div>
    </>
  );
}

export default App;
