import React from 'react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatCurrency } from '../../utils/formatters';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        backgroundColor: 'var(--bg-3)',
        border: '1px solid var(--border)',
        padding: '12px',
        borderRadius: '8px',
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-sm)',
        color: 'var(--text-1)'
      }}>
        <div style={{ color: 'var(--text-3)', fontSize: 'var(--text-xs)', fontFamily: 'var(--font-ui)', marginBottom: '4px', textTransform: 'uppercase' }}>
          {payload[0].payload.name}
        </div>
        ${formatCurrency(payload[0].value)}
      </div>
    );
  }
  return null;
};

const CustomLabel = (props) => {
  const { x, y, width, value } = props;
  return (
    <text
      x={x + width / 2}
      y={y - 12}
      fill="var(--text-2)"
      textAnchor="middle"
      fontSize="var(--text-xs)"
      fontFamily="var(--font-mono)"
    >
      ${formatCurrency(value)}
    </text>
  );
};

const AmountBarChart = ({ invoiceTotal, poTotal }) => {
  const data = [
    { name: 'Invoice', value: invoiceTotal },
    { name: 'PO', value: poTotal }
  ];

  return (
    <div style={{ height: 200, width: '100%' }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{ top: 30, right: 30, left: 30, bottom: 0 }}
        >
          <XAxis 
            dataKey="name" 
            axisLine={{ stroke: 'var(--border)' }} 
            tickLine={false}
            tick={{ fill: 'var(--text-3)', fontSize: 'var(--text-xs)', fontFamily: 'var(--font-ui)', dy: 10 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--bg-3)', opacity: 0.5 }} />
          <Bar 
            dataKey="value" 
            barSize={48}
            isAnimationActive={true}
            animationDuration={800}
            animationEasing="ease-out"
            label={<CustomLabel />}
          >
            {data.map((entry, index) => {
              if (entry.name === 'Invoice') {
                return <Cell key={`cell-${index}`} fill="var(--blue)" />;
              }
              return (
                <Cell 
                  key={`cell-${index}`} 
                  fill="var(--text-2)" 
                  stroke="var(--bg-4)" 
                  strokeWidth={2} 
                />
              );
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AmountBarChart;
