import { useEffect, useState } from "react";
import { mySalarySlips } from "../../api/endpoints";

const monthNames = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export default function MySalary() {
  const [slips, setSlips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    mySalarySlips().then(setSlips).finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2 className="font-serif text-lg text-ink mb-6">My Salary Slips</h2>

      {loading && <p className="text-sm text-ink-muted">Loading…</p>}
      {!loading && slips.length === 0 && (
        <p className="text-sm text-ink-muted">No salary slips generated yet.</p>
      )}

      <div className="grid grid-cols-2 gap-5">
        {slips.map((slip) => (
          <div key={slip.id} className="bg-surface rounded-card shadow-card p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-serif text-lg text-ink">
                {monthNames[slip.month]} {slip.year}
              </h3>
              <span className="font-mono text-2xl text-signal">₹{slip.net_salary}</span>
            </div>
            <div className="space-y-2 text-sm">
              <Row label="Base Salary" value={`₹${slip.base_salary}`} />
              <Row label="Days Present" value={slip.days_present} />
              <Row label="Days Absent" value={slip.days_absent} />
              <Row label="Deduction" value={`− ₹${slip.deduction}`} tone="clay" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Row({ label, value, tone }) {
  return (
    <div className="flex justify-between border-b border-line pb-2">
      <span className="text-ink-muted">{label}</span>
      <span className={`font-mono ${tone === "clay" ? "text-clay" : "text-ink"}`}>{value}</span>
    </div>
  );
}
