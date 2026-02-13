import React from 'react';
import './ResultsSection.css';

const ResultsSection = ({ result }) => {
    if (!result) return null;

    const {
        summary,
        line_item_analysis,
        confidence_score,
        risk_score,
        risk_reason,
        processing_time_ms,
        duplicate
    } = result;

    // --- Helpers for Styling ---
    const getConfidenceColor = (score) => {
        if (!score) return 'gray';
        if (score > 85) return 'green';
        if (score >= 70) return 'yellow';
        return 'red';
    };

    const getRiskColor = (score) => {
        if (score <= 30) return 'green';
        if (score <= 70) return 'orange';
        return 'red';
    };

    const getStatusColor = (status) => {
        switch (status?.toLowerCase()) {
            case 'match': return 'green';
            case 'quantity_mismatch': return 'orange';
            case 'price_mismatch': return 'orange';
            case 'missing_in_po': return 'red';
            case 'extra_in_invoice': return 'red';
            case 'extra_in_po': return 'blue';
            default: return 'gray';
        }
    };

    return (
        <div className="results-container">
            {/* 5️⃣ Duplicate Warning */}
            {duplicate && (
                <div className="duplicate-banner">
                    ⚠️ Document previously processed (served from cache)
                </div>
            )}

            <div className="metrics-grid">
                {/* 1️⃣ Structured Summary */}
                <div className="card summary-card">
                    <h3>Comparison Summary</h3>
                    <div className="summary-row">
                        <span>Invoice Total:</span>
                        <strong>{summary?.invoice_total?.toFixed(2) ?? 'N/A'}</strong>
                    </div>
                    <div className="summary-row">
                        <span>PO Total:</span>
                        <strong>{summary?.po_total?.toFixed(2) ?? 'N/A'}</strong>
                    </div>
                    <div className="summary-row">
                        <span>Difference:</span>
                        <strong className={summary?.difference === 0 ? 'text-green' : 'text-red'}>
                            {summary?.difference?.toFixed(2) ?? 'N/A'}
                        </strong>
                    </div>
                    <div className={`status-badge ${summary?.status === 'match' ? 'bg-green' : 'bg-red'}`}>
                        {summary?.status?.toUpperCase()}
                    </div>
                </div>

                {/* 3️⃣ Confidence & 4️⃣ Risk */}
                <div className="card scores-card">
                    <h3>AI Analysis</h3>

                    <div className="score-item">
                        <span>Confidence Score</span>
                        <div className={`badge ${getConfidenceColor(confidence_score)}`}>
                            {confidence_score ? `${confidence_score}%` : 'N/A'}
                        </div>
                    </div>

                    <div className="score-item">
                        <span>Risk Score</span>
                        <div className={`badge ${getRiskColor(risk_score)}`}>
                            {risk_score}/100
                        </div>
                    </div>

                    {risk_reason && (
                        <div className="risk-reason">
                            <strong>Risk Factor:</strong> {risk_reason}
                        </div>
                    )}

                    {/* 6️⃣ Processing Time */}
                    <div className="processing-time">
                        ⏱ Processed in {processing_time_ms?.toFixed(0)} ms
                    </div>
                </div>
            </div>

            {/* 2️⃣ Line Item Analysis Table */}
            <div className="card table-card">
                <h3>Line Item Analysis</h3>
                <div className="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Description</th>
                                <th>Inv Qty</th>
                                <th>PO Qty</th>
                                <th>Inv Price</th>
                                <th>PO Price</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {line_item_analysis?.map((item, index) => (
                                <tr key={index} className={`row-${getStatusColor(item.status)}`}>
                                    <td>{item.description}</td>
                                    <td>{item.invoice_qty ?? '-'}</td>
                                    <td>{item.po_qty ?? '-'}</td>
                                    <td>{item.invoice_price?.toFixed(2) ?? '-'}</td>
                                    <td>{item.po_price?.toFixed(2) ?? '-'}</td>
                                    <td>
                                        <span className={`status-tag ${getStatusColor(item.status)}`}>
                                            {item.status.replace(/_/g, ' ')}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ResultsSection;
