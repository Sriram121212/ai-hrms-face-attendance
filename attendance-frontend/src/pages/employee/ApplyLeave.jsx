import { useEffect, useState } from "react";
import { applyLeave, myLeaves } from "../../api/endpoints";

const statusStyles = {
  pending: "bg-amber-soft text-amber",
  approved: "bg-signal-soft text-signal",
  rejected: "bg-clay-soft text-clay",
};

export default function ApplyLeave() {
  const [form, setForm] = useState({ from_date: "", to_date: "", reason: "" });
  const [leaves, setLeaves] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // const load = () => myLeaves().then(setLeaves).finally(() => setLoading(false));
  // useEffect(load, []);

const load = () => myLeaves().then(setLeaves).finally(() => setLoading(false));
useEffect(() => {
  load();
}, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await applyLeave(form);
      setForm({ from_date: "", to_date: "", reason: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not submit leave request");
    }
  };

  return (
    <div className="grid grid-cols-3 gap-6">
      <form onSubmit={handleSubmit} className="col-span-1 bg-surface rounded-card shadow-card p-6 h-fit">
        <h2 className="font-serif text-lg text-ink mb-4">Apply for Leave</h2>
        {error && <p className="text-clay text-sm mb-3">{error}</p>}

        <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">From</label>
        <input
          type="date"
          required
          value={form.from_date}
          onChange={(e) => setForm({ ...form, from_date: e.target.value })}
          className="w-full px-3 py-2 mb-4 rounded-card border border-line text-sm font-mono"
        />

        <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">To</label>
        <input
          type="date"
          required
          value={form.to_date}
          onChange={(e) => setForm({ ...form, to_date: e.target.value })}
          className="w-full px-3 py-2 mb-4 rounded-card border border-line text-sm font-mono"
        />

        <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">Reason</label>
        <textarea
          required
          rows={3}
          value={form.reason}
          onChange={(e) => setForm({ ...form, reason: e.target.value })}
          className="w-full px-3 py-2 mb-4 rounded-card border border-line text-sm"
        />

        <button type="submit" className="w-full bg-ink text-white py-2.5 rounded-card text-sm hover:bg-ink-light transition-colors">
          Submit Request
        </button>
      </form>

      <div className="col-span-2 bg-surface rounded-card shadow-card p-6">
        <h3 className="font-serif text-lg text-ink mb-4">Your Leave History</h3>
        {loading && <p className="text-sm text-ink-muted">Loading…</p>}
        {!loading && leaves.length === 0 && <p className="text-sm text-ink-muted">No leave requests yet.</p>}
        {!loading && leaves.map((lv) => (
          <div key={lv.id} className="flex items-center justify-between py-3 border-b border-line last:border-0">
            <div>
              <p className="text-sm text-ink font-mono">{lv.from_date} → {lv.to_date}</p>
              <p className="text-xs text-ink-muted mt-0.5">{lv.reason}</p>
            </div>
            <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${statusStyles[lv.status]}`}>
              {lv.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
