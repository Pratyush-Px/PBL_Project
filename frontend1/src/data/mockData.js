export const MOCK_DETAILS = {
  "1": {
    id: "1",
    order_id: "1001",
    match_status: "match",
    risk_score: 0,
    confidence_score: 94,
    created_at: "2026-03-30T10:15:00Z",
    result_json: {
      summary: { invoice_total: 8450.00, po_total: 8450.00, difference: 0, status: "match" },
      line_item_analysis: [
        { description: "ThinkPad X1 Carbon Gen 10", invoice_qty: 2, po_qty: 2, invoice_price: 2400.00, po_price: 2400.00, status: "match" },
        { description: "Dell UltraSharp 27 Monitor", invoice_qty: 4, po_qty: 4, invoice_price: 450.00, po_price: 450.00, status: "match" },
        { description: "Logitech MX Master 3S", invoice_qty: 6, po_qty: 6, invoice_price: 100.00, po_price: 100.00, status: "match" },
        { description: "Keychron K8 Pro", invoice_qty: 6, po_qty: 6, invoice_price: 125.00, po_price: 125.00, status: "match" },
        { description: "CalDigit TS4 Dock", invoice_qty: 1, po_qty: 1, invoice_price: 400.00, po_price: 400.00, status: "match" },
        { description: "Laptop Stand Aluminum", invoice_qty: 2, po_qty: 2, invoice_price: 50.00, po_price: 50.00, status: "match" }
      ],
      confidence_score: 94,
      risk_score: 0,
      risk_reason: "No issues detected",
      processing_time_ms: 1240
    }
  },
  "2": {
    id: "2",
    order_id: "1002",
    match_status: "mismatch",
    risk_score: 60,
    confidence_score: 81,
    created_at: "2026-03-30T11:20:00Z",
    result_json: {
      summary: { invoice_total: 12300.00, po_total: 10800.00, difference: 1500.00, status: "mismatch" },
      line_item_analysis: [
        { description: "Herman Miller Aeron", invoice_qty: 4, po_qty: 3, invoice_price: 1500.00, po_price: 1500.00, status: "quantity_mismatch" },
        { description: "Steelcase Gesture", invoice_qty: 1, po_qty: 2, invoice_price: 1400.00, po_price: 1400.00, status: "quantity_mismatch" },
        { description: "Uplift V2 Standing Desk", invoice_qty: 4, po_qty: 4, invoice_price: 1000.00, po_price: 800.00, status: "price_mismatch" },
        { description: "Monitor Arm Dual", invoice_qty: 2, po_qty: 2, invoice_price: 250.00, po_price: 250.00, status: "match" },
        { description: "Cable Management Tray", invoice_qty: 4, po_qty: 4, invoice_price: 100.00, po_price: 100.00, status: "match" }
      ],
      confidence_score: 81,
      risk_score: 60,
      risk_reason: "Quantity mismatch on Aeron chair;Quantity mismatch on Gesture chair;Price discrepancy on Standing Desk",
      processing_time_ms: 1530
    }
  },
  "3": {
    id: "3",
    order_id: "1003",
    match_status: "mismatch",
    risk_score: 100,
    confidence_score: 52,
    created_at: "2026-03-30T12:05:00Z",
    result_json: {
      summary: { invoice_total: 6200.00, po_total: 4900.00, difference: 1300.00, status: "mismatch" },
      line_item_analysis: [
        { description: "Cisco Catalyst 9200", invoice_qty: 1, po_qty: 1, invoice_price: 2500.00, po_price: 2500.00, status: "match" },
        { description: "Ubiquiti UniFi Pro AP", invoice_qty: 0, po_qty: 3, invoice_price: 0, po_price: 300.00, status: "missing_in_po" },
        { description: "Netgear 10G Switch", invoice_qty: 2, po_qty: 0, invoice_price: 900.00, po_price: 0, status: "extra_in_po" },
        { description: "Cat6 Ethernet Spool", invoice_qty: 5, po_qty: 2, invoice_price: 400.00, po_price: 400.00, status: "quantity_mismatch" },
        { description: "Patch Panels", invoice_qty: 2, po_qty: 0, invoice_price: 250.00, po_price: 0, status: "extra_in_invoice" },
        { description: "Server Rack 42U", invoice_qty: 0, po_qty: 1, invoice_price: 0, po_price: 700.00, status: "missing_in_po" }
      ],
      confidence_score: 52,
      risk_score: 100,
      risk_reason: "High number of discrepancies;Missing line items in PO;Extra unauthorized items billed;Large quantity mismatch",
      processing_time_ms: 2110
    }
  },
  "4": {
    id: "4",
    order_id: "1004",
    match_status: "match",
    risk_score: 0,
    confidence_score: 97,
    created_at: "2026-03-30T12:45:00Z",
    result_json: {
      summary: { invoice_total: 1240.00, po_total: 1240.00, difference: 0, status: "match" },
      line_item_analysis: [
        { description: "Printer Paper Carton", invoice_qty: 10, po_qty: 10, invoice_price: 45.00, po_price: 45.00, status: "match" },
        { description: "Toner Box Black", invoice_qty: 4, po_qty: 4, invoice_price: 110.00, po_price: 110.00, status: "match" },
        { description: "Whiteboard Markers Set", invoice_qty: 20, po_qty: 20, invoice_price: 17.50, po_price: 17.50, status: "match" }
      ],
      confidence_score: 97,
      risk_score: 0,
      risk_reason: "No issues detected",
      processing_time_ms: 870
    }
  },
  "5": {
    id: "5",
    order_id: "1005",
    match_status: "mismatch",
    risk_score: 40,
    confidence_score: 76,
    created_at: "2026-03-30T13:30:00Z",
    result_json: {
      summary: { invoice_total: 5680.00, po_total: 5210.00, difference: 470.00, status: "mismatch" },
      line_item_analysis: [
        { description: "Apple Magic Keyboard", invoice_qty: 10, po_qty: 10, invoice_price: 120.00, po_price: 150.00, status: "price_mismatch" },
        { description: "Apple Magic Mouse", invoice_qty: 10, po_qty: 10, invoice_price: 80.00, po_price: 80.00, status: "match" },
        { description: "Anker USB-C Hub", invoice_qty: 20, po_qty: 20, invoice_price: 45.00, po_price: 45.00, status: "match" },
        { description: "Macbook Air M2", invoice_qty: 2, po_qty: 2, invoice_price: 1100.00, po_price: 1100.00, status: "match" },
        { description: "Extended Warranty", invoice_qty: 2, po_qty: 0, invoice_price: 385.00, po_price: 0, status: "extra_in_invoice" }
      ],
      confidence_score: 76,
      risk_score: 40,
      risk_reason: "Keyboard price underbilled vs PO;Unauthorized extended warranty billed",
      processing_time_ms: 1450
    }
  },
  "6": {
    id: "6",
    order_id: "1006",
    match_status: "mismatch",
    risk_score: 70,
    confidence_score: 68,
    created_at: "2026-03-30T14:15:00Z",
    result_json: {
      summary: { invoice_total: 18900.00, po_total: 16500.00, difference: 2400.00, status: "mismatch" },
      line_item_analysis: [
        { description: "Dell PowerEdge R750", invoice_qty: 2, po_qty: 2, invoice_price: 5500.00, po_price: 5500.00, status: "match" },
        { description: "NVIDIA A100 GPU", invoice_qty: 1, po_qty: 0, invoice_price: 6800.00, po_price: 0, status: "missing_in_po" },
        { description: "64GB DDR4 ECC RAM", invoice_qty: 4, po_qty: 8, invoice_price: 150.00, po_price: 150.00, status: "quantity_mismatch" },
        { description: "2TB NVMe SSD", invoice_qty: 4, po_qty: 4, invoice_price: 250.00, po_price: 250.00, status: "match" }
      ],
      confidence_score: 68,
      risk_score: 70,
      risk_reason: "High-value GPU missing from original PO;RAM quantity under-delivered vs PO",
      processing_time_ms: 1980
    }
  }
};

export const MOCK_RESULTS = Object.values(MOCK_DETAILS).map(detail => ({
  id: detail.id,
  order_id: detail.order_id,
  match_status: detail.match_status,
  risk_score: detail.risk_score,
  confidence_score: detail.confidence_score,
  created_at: detail.created_at
}));
