import React, { useMemo } from 'react';
import {
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
} from 'recharts';
import { motion } from 'framer-motion';
import { countLineItemMatches, extractMismatchTypes, buildFieldComparison } from '../utils/analytics';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: 'rgba(255, 255, 255, 0.95)', padding: '10px 14px', border: '1px solid var(--border-light)', borderRadius: '10px', boxShadow: 'var(--shadow-floating)' }}>
        <p style={{ margin: 0, color: 'var(--text-primary)', fontWeight: 600, fontSize: '0.85rem' }}>
          {`${payload[0].name || payload[0].payload.name} : ${payload[0].value}`}
        </p>
      </div>
    );
  }
  return null;
};

/**
 * DetailCharts: Per-comparison analytics charts.
 * Receives lineItems (result_json.line_item_analysis) as prop.
 */
const DetailCharts = ({ lineItems }) => {
  // 1. Line Item Match vs Mismatch
  const lineMatchData = useMemo(() => countLineItemMatches(lineItems), [lineItems]);

  // 2. Mismatch Categories
  const mismatchTypes = useMemo(() => extractMismatchTypes(lineItems), [lineItems]);

  // 3. Field-Level Price Comparison
  const fieldCompData = useMemo(() => buildFieldComparison(lineItems), [lineItems]);

  if (!lineItems || lineItems.length === 0) return null;

  const matchPercentage = useMemo(() => {
    const matched = lineMatchData.find(d => d.name === 'Matched')?.value || 0;
    const total = lineMatchData.reduce((acc, d) => acc + d.value, 0);
    return total > 0 ? Math.round((matched / total) * 100) : 0;
  }, [lineMatchData]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.5 }}
      style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '24px' }}
    >
      {/* ── Line Item Match/Mismatch Donut ── */}
      {lineMatchData.length > 0 && (
        <div className="card-premium" style={{ padding: '20px' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '16px' }}>
            Line Item Status
          </h4>
          <div style={{ height: '220px', position: 'relative' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={lineMatchData} innerRadius={50} outerRadius={75} paddingAngle={6} dataKey="value" stroke="none" animationDuration={1200}>
                  {lineMatchData.map((entry, i) => (
                    <Cell key={`lm-${i}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend verticalAlign="bottom" height={30} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ position: 'absolute', top: '42%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{matchPercentage}%</div>
              <div style={{ fontSize: '0.6rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Match</div>
            </div>
          </div>
        </div>
      )}

      {/* ── Mismatch Categories Bar ── */}
      {mismatchTypes.length > 0 && (
        <div className="card-premium" style={{ padding: '20px' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '16px' }}>
            Mismatch Categories
          </h4>
          <div style={{ height: '220px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mismatchTypes} margin={{ top: 5, right: 5, left: -25, bottom: 0 }} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" horizontal={false} />
                <XAxis type="number" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
                <YAxis dataKey="name" type="category" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} width={110} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={24} animationDuration={1200}>
                  {mismatchTypes.map((entry, i) => (
                    <Cell key={`mt-${i}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* ── Field-Level Price Comparison ── */}
      {fieldCompData.length > 0 && (
        <div className="card-premium" style={{ padding: '20px', gridColumn: fieldCompData.length > 3 ? '1 / -1' : 'auto' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '16px' }}>
            Invoice vs PO Price Comparison
          </h4>
          <div style={{ height: '240px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={fieldCompData} margin={{ top: 5, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={10} tickLine={false} axisLine={false} angle={-15} textAnchor="end" />
                <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
                <RechartsTooltip
                  contentStyle={{ background: 'rgba(255,255,255,0.95)', border: '1px solid var(--border-light)', borderRadius: '10px' }}
                  labelStyle={{ fontWeight: 600, color: 'var(--text-primary)' }}
                />
                <Legend verticalAlign="top" height={30} iconType="circle" />
                <Bar dataKey="invoice" name="Invoice Price" fill="#4f46e5" radius={[4, 4, 0, 0]} barSize={20} animationDuration={1200} />
                <Bar dataKey="po" name="PO Price" fill="#22c55e" radius={[4, 4, 0, 0]} barSize={20} animationDuration={1200} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default DetailCharts;
