import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

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
        <div style={{ color: 'var(--text-3)', fontSize: 'var(--text-xs)', fontFamily: 'var(--font-ui)', marginBottom: '4px' }}>
          #{payload[0].payload.orderId}
        </div>
        Score: {payload[0].value}
      </div>
    );
  }
  return null;
};

const RiskAreaChart = ({ data, selectedOrderId }) => {
  // Add a gradient id for area fill
  const gradientId = "riskGradient";

  return (
    <div style={{ height: 180, width: '100%' }}>
      <ResponsiveContainer>
        <AreaChart
          data={data}
          margin={{ top: 10, right: 0, left: -20, bottom: 0 }}
        >
          <defs>
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="var(--blue)" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="var(--blue)" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="none" />
          <XAxis 
            dataKey="shortId" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--text-3)', fontSize: 'var(--text-xs)', fontFamily: 'var(--font-mono)', dy: 10 }}
          />
          <YAxis 
            ticks={[0, 50, 100]}
            domain={[0, 100]}
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--text-3)', fontSize: 'var(--text-xs)', fontFamily: 'var(--font-ui)', dx: -10 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine 
            x={data.find(d => d.orderId === selectedOrderId)?.shortId} 
            stroke="rgba(255,255,255,0.1)" 
            strokeDasharray="none" 
          />
          <Area 
            type="monotone" 
            dataKey="score" 
            stroke="var(--blue)" 
            strokeWidth={2}
            fillOpacity={1} 
            fill={`url(#${gradientId})`} 
            isAnimationActive={true}
            animationDuration={1000}
            activeDot={{ r: 6, fill: "var(--blue)", stroke: "#fff", strokeWidth: 2 }}
            dot={{ r: 3, fill: "var(--blue)", strokeWidth: 0 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskAreaChart;
