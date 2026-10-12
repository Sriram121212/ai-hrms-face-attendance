import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import StatCard from "../../components/StatCard";
import { getCostSummary, getRecentChatLogs } from "../../api/endpoints";

const FEATURE_LABELS = {
  hr_policy_rag: "HR Policy RAG",
  admin_agent: "AI Admin Agent",
};

const FEATURE_COLORS = {
  hr_policy_rag: "#1F8A57",
  admin_agent: "#C98A2E",
};

const typeStyles = {
  hr_policy_rag: "bg-signal-soft text-signal",
  admin_agent: "bg-amber-soft text-amber",
};

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="bg-ink text-white text-xs px-3 py-2 rounded-card shadow-card">
      <p className="font-medium mb-1">{d.label}</p>
      <p>{d.query_count} queries</p>
      <p>{d.total_tokens.toLocaleString()} tokens</p>
      <p className="font-mono">${d.total_cost.toFixed(4)}</p>
    </div>
  );
}

export default function CostTracker() {
  const [summary, setSummary] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCostSummary(), getRecentChatLogs(30)])
      .then(([s, l]) => {
        setSummary(s);
        setLogs(l);
      })
      .finally(() => setLoading(false));
  }, []);

  const chartData = (summary?.by_type || []).map((t) => ({
    label: FEATURE_LABELS[t.chat_type] || t.chat_type,
    chat_type: t.chat_type,
    total_cost: t.total_cost,
    total_tokens: t.total_tokens,
    query_count: t.query_count,
  }));

  return (
    <div>
      <h2 className="font-serif text-lg text-ink mb-1">GenAI Cost Tracker</h2>
      <p className="text-sm text-ink-muted mb-6">
        Token and cost usage across the RAG chatbot and the AI admin agent.
      </p>

      {loading && <p className="text-sm text-ink-muted">Loading…</p>}

      {!loading && summary && (
        <>
          <div className="flex gap-4 mb-8 flex-wrap">
            <StatCard label="Total Queries" value={summary.total_queries} />
            <StatCard label="Total Tokens" value={summary.total_tokens.toLocaleString()} />
            <StatCard label="Total Cost" value={`$${summary.total_cost.toFixed(4)}`} tone="signal" />
          </div>

          <div className="grid grid-cols-2 gap-6 mb-6">
            <div className="bg-surface rounded-card shadow-card p-6">
              <h3 className="font-serif text-base text-ink mb-4">Cost by Feature</h3>
              {chartData.length === 0 ? (
                <p className="text-sm text-ink-muted">No usage yet.</p>
              ) : (
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={chartData} layout="vertical" margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#DDE3E1" horizontal={false} />
                    <XAxis type="number" tick={{ fontSize: 11, fill: "#5B6B7A" }} tickFormatter={(v) => `$${v}`} />
                    <YAxis type="category" dataKey="label" tick={{ fontSize: 12, fill: "#14202E" }} width={110} />
                    <Tooltip content={<CustomTooltip />} cursor={{ fill: "#F1F4F3" }} />
                    <Bar dataKey="total_cost" radius={[0, 6, 6, 0]} barSize={28}>
                      {chartData.map((entry) => (
                        <Cell key={entry.chat_type} fill={FEATURE_COLORS[entry.chat_type] || "#14202E"} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="bg-surface rounded-card shadow-card p-6">
              <h3 className="font-serif text-base text-ink mb-4">Breakdown</h3>
              {summary.by_type.length === 0 && <p className="text-sm text-ink-muted">No usage yet.</p>}
              {summary.by_type.map((t) => (
                <div key={t.chat_type} className="flex items-center justify-between py-3 border-b border-line last:border-0">
                  <div>
                    <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${typeStyles[t.chat_type]}`}>
                      {FEATURE_LABELS[t.chat_type] || t.chat_type}
                    </span>
                    <p className="text-xs text-ink-muted mt-1">{t.query_count} queries · {t.total_tokens.toLocaleString()} tokens</p>
                  </div>
                  <span className="font-mono text-ink">${t.total_cost.toFixed(4)}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-surface rounded-card shadow-card overflow-hidden">
            <div className="px-6 py-4 border-b border-line">
              <h3 className="font-serif text-base text-ink">Recent Queries</h3>
            </div>
            <table className="w-full text-sm">
              <thead className="bg-canvas text-ink-muted text-xs uppercase tracking-wider">
                <tr>
                  <th className="text-left px-5 py-3">Employee</th>
                  <th className="text-left px-5 py-3">Feature</th>
                  <th className="text-left px-5 py-3">Query</th>
                  <th className="text-right px-5 py-3">Tokens</th>
                  <th className="text-right px-5 py-3">Cost</th>
                  <th className="text-right px-5 py-3">Time</th>
                </tr>
              </thead>
              <tbody>
                {logs.length === 0 && (
                  <tr><td colSpan={6} className="px-5 py-4 text-ink-muted">No queries logged yet.</td></tr>
                )}
                {logs.map((log) => (
                  <tr key={log.id} className="border-t border-line">
                    <td className="px-5 py-3 text-ink font-medium">{log.employee_name}</td>
                    <td className="px-5 py-3">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${typeStyles[log.chat_type]}`}>
                        {FEATURE_LABELS[log.chat_type] || log.chat_type}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-ink-muted max-w-xs truncate">{log.query}</td>
                    <td className="px-5 py-3 text-right font-mono">{log.tokens_used}</td>
                    <td className="px-5 py-3 text-right font-mono">${log.cost_usd.toFixed(5)}</td>
                    <td className="px-5 py-3 text-right text-xs text-ink-muted font-mono">
                      {new Date(log.created_at).toLocaleString("en-IN", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}