import React, { useMemo } from 'react';
import { 
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
  LineChart, Line
} from 'recharts';
import { motion } from 'framer-motion';
import { groupByDate, countMatches, calculateRiskBuckets, countHighVsLowRisk } from '../utils/analytics';

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: 'rgba(255, 255, 255, 0.95)', padding: '12px 16px', border: '1px solid var(--border-light)', borderRadius: '12px', boxShadow: 'var(--shadow-floating)', backdropFilter: 'blur(10px)' }}>
        <p style={{ margin: 0, color: 'var(--text-primary)', fontWeight: 600, fontSize: '0.95rem' }}>
          {`${payload[0].name || payload[0].payload.name || payload[0].payload.date} : ${payload[0].value}`}
        </p>
      </div>
    );
  }
  return null;
};

const Visualizations = ({ results }) => {
  // 1. Match vs Mismatch Donut data
  const { match, mismatch } = useMemo(() => countMatches(results), [results]);
  const matchData = useMemo(() => [
    { name: 'Match', value: match, color: '#22c55e' },
    { name: 'Mismatch', value: mismatch, color: '#ef4444' }
  ], [match, mismatch]);
  const matchPercentage = useMemo(() => {
    const total = match + mismatch;
    return total === 0 ? 0 : Math.round((match / total) * 100);
  }, [match, mismatch]);

  // 2. Risk Distribution data
  const riskBuckets = useMemo(() => calculateRiskBuckets(results), [results]);
  const riskData = useMemo(() => [
    { name: 'Low (0-30)', count: riskBuckets.low, fill: '#22c55e' },
    { name: 'Med (31-70)', count: riskBuckets.medium, fill: '#f59e0b' },
    { name: 'High (71-100)', count: riskBuckets.high, fill: '#ef4444' }
  ], [riskBuckets]);

  // 3. Trend data (comparisons per day + avg risk per day)
  const trendData = useMemo(() => groupByDate(results), [results]);

  // 4. High Risk vs Low Risk data
  const highLowData = useMemo(() => countHighVsLowRisk(results), [results]);

  return (
    <div className="charts-grid">
      {/* ── Chart 1: Match vs Mismatch Donut ── */}
      <motion.div variants={itemVariants} initial="hidden" whileInView="show" viewport={{ once: true, margin: "-50px" }} className="chart-card card-premium">
        <div className="chart-header">
          <h3 className="chart-title">Match Rate Overview</h3>
        </div>
        <div className="chart-wrapper" style={{ position: 'relative' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={matchData} innerRadius={75} outerRadius={105} paddingAngle={6} dataKey="value" stroke="none" animationDuration={1500} animationEasing="ease-out">
                {matchData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <RechartsTooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" height={36} iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ position: 'absolute', top: '45%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none' }}>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{matchPercentage}%</div>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Success</div>
          </div>
        </div>
      </motion.div>

      {/* ── Chart 2: Risk Distribution Bar ── */}
      <motion.div variants={itemVariants} initial="hidden" whileInView="show" viewport={{ once: true, margin: "-50px" }} className="chart-card card-premium">
        <div className="chart-header">
          <h3 className="chart-title">Risk Distribution</h3>
        </div>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={riskData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dy={8} />
              <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dx={-8} allowDecimals={false} />
              <RechartsTooltip content={<CustomTooltip />} cursor={{fill: 'rgba(0,0,0,0.03)'}} />
              <Bar dataKey="count" radius={[8, 8, 8, 8]} barSize={48} animationDuration={1500}>
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* ── Chart 3: Comparisons Over Time ── */}
      <motion.div variants={itemVariants} initial="hidden" whileInView="show" viewport={{ once: true, margin: "-50px" }} className="chart-card card-premium">
        <div className="chart-header">
          <h3 className="chart-title">Comparisons Over Time</h3>
        </div>
        <div className="chart-wrapper">
          {trendData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" vertical={false} />
                <XAxis dataKey="date" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dy={10} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dx={-10} allowDecimals={false} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="comparisons" name="Comparisons" stroke="var(--primary)" strokeWidth={3} dot={{ r: 4, fill: 'var(--primary)', strokeWidth: 0 }} activeDot={{ r: 8, fill: 'var(--primary)', stroke: '#fff', strokeWidth: 3 }} animationDuration={2000} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div style={{display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)'}}>Awaiting more temporal data...</div>
          )}
        </div>
      </motion.div>

      {/* ── Chart 4: Average Risk Over Time ── */}
      <motion.div variants={itemVariants} initial="hidden" whileInView="show" viewport={{ once: true, margin: "-50px" }} className="chart-card card-premium">
        <div className="chart-header">
          <h3 className="chart-title">Avg Risk Trend</h3>
        </div>
        <div className="chart-wrapper">
          {trendData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" vertical={false} />
                <XAxis dataKey="date" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dy={10} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dx={-10} domain={[0, 100]} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="avgRisk" name="Avg Risk" stroke="#ef4444" strokeWidth={3} dot={{ r: 4, fill: '#ef4444', strokeWidth: 0 }} activeDot={{ r: 8, fill: '#ef4444', stroke: '#fff', strokeWidth: 3 }} animationDuration={2000} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div style={{display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)'}}>Awaiting more temporal data...</div>
          )}
        </div>
      </motion.div>

      {/* ── Chart 5: High Risk vs Normal (Pie) ── */}
      <motion.div variants={itemVariants} initial="hidden" whileInView="show" viewport={{ once: true, margin: "-50px" }} className="chart-card card-premium full-span">
        <div className="chart-header">
          <h3 className="chart-title">Risk Exposure Overview</h3>
        </div>
        <div className="chart-wrapper" style={{ position: 'relative' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={highLowData} innerRadius={65} outerRadius={100} paddingAngle={6} dataKey="value" stroke="none" animationDuration={1500}>
                {highLowData.map((entry, index) => (
                  <Cell key={`cell-hl-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <RechartsTooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" height={36} iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ position: 'absolute', top: '45%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none' }}>
            <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{highLowData[0]?.value || 0}</div>
            <div style={{ fontSize: '0.7rem', fontWeight: 600, color: '#ef4444', textTransform: 'uppercase', letterSpacing: '0.05em' }}>High Risk</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Visualizations;
