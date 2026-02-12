import React from 'react';
import './DifferencesTable.css';

const DifferencesTable = ({ differences }) => {
    if (!differences || differences.length === 0) {
        return (
            <div className="no-differences">
                <p>✅ No discrepancies found. Documents match perfectly.</p>
            </div>
        );
    }

    return (
        <div className="differences-table-container">
            <h3>Discrepancies Found</h3>
            <table className="differences-table">
                <thead>
                    <tr>
                        <th>Field</th>
                        <th>Order Value</th>
                        <th>Invoice Value</th>
                    </tr>
                </thead>
                <tbody>
                    {differences.map((diff, index) => (
                        <tr key={index}>
                            <td className="field-name">{diff.field}</td>
                            <td className="order-value">{String(diff.order_value)}</td>
                            <td className="invoice-value">{String(diff.invoice_value)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default DifferencesTable;
