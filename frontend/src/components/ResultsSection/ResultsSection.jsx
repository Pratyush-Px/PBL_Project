import React from 'react';
import DifferencesTable from '../DifferencesTable/DifferencesTable';
import DocumentViewer from '../DocumentViewer/DocumentViewer';
import './ResultsSection.css';

const ResultsSection = ({ result }) => {
    if (!result) return null;

    const { comparison, order_data, invoice_data } = result;

    // Safeguard against missing comparison data
    if (!comparison) return null;

    const isMatch = comparison.status === "Match";
    const matchPercentage = comparison.match_percentage || 0;

    const downloadReport = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "comparison_report.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    return (
        <div className="results-section">
            <div className="results-header">
                <h2>Comparison Results</h2>
                <button className="download-btn" onClick={downloadReport}>
                    Download Report ⬇️
                </button>
            </div>

            <div className="status-card">
                <div className={`status-badge ${isMatch ? 'match' : 'mismatch'}`}>
                    {comparison.status}
                </div>
                <div className="match-percentage">
                    <span>Match Score: {matchPercentage}%</span>
                    <div className="progress-bar-bg">
                        <div
                            className={`progress-bar-fill ${isMatch ? 'high' : 'low'}`}
                            style={{ width: `${matchPercentage}%` }}
                        ></div>
                    </div>
                </div>
            </div>

            <DifferencesTable differences={comparison.differences} />

            <div className="json-viewers">
                <DocumentViewer title="Extracted Order Data" data={order_data} />
                <DocumentViewer title="Extracted Invoice Data" data={invoice_data} />
            </div>
        </div>
    );
};

export default ResultsSection;
