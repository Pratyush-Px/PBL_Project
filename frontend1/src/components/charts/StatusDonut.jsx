import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { getStatusColors } from '../../utils/colors';

const StatusDonut = ({ data }) => {
  // Filter out any 0 count items
  const activeData = data.filter(d => d.value > 0);
  const totalItems = activeData.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <div>
      <div style={{ height: '220px', width: '100%', position: 'relative' }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={activeData}
              innerRadius={60}
              outerRadius={90}
              dataKey="value"
              stroke="var(--bg-2)"
              strokeWidth={3}
              isAnimationActive={true}
              animationDuration={700}
            >
              {activeData.map((entry, index) => {
                const colors = getStatusColors(entry.name);
                return <Cell key={`cell-${index}`} fill={colors.color} />;
              })}
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        {/* Center label overlay */}
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          pointerEvents: 'none'
        }}>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontWeight: 300,
            fontSize: '28px',
            color: 'var(--text-1)',
            letterSpacing: '-0.02em'
          }}>
            {totalItems}
          </span>
        </div>
      </div>

      {/* Custom Legend */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
        marginTop: 'var(--space-4)'
      }}>
        {activeData.map((entry, idx) => {
          const colors = getStatusColors(entry.name);
          return (
            <div key={idx} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontFamily: 'var(--font-ui)',
              fontSize: 'var(--text-sm)',
              color: 'var(--text-2)'
            }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: colors.color }} />
              {colors.label} <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-1)' }}>{entry.value}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusDonut;
