import { useEffect, useState } from "react";
import { allLeaves, approveLeave, rejectLeave, listEmployees } from "../../api/endpoints";

const statusStyles = {
  pending: "bg-amber-soft text-amber",
  approved: "bg-signal-soft text-signal",
  rejected: "bg-clay-soft text-clay",
};

export default function LeaveApprovals() {
  const [leaves, setLeaves] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [filter, setFilter] = useState("pending");
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    Promise.all([allLeaves(filter === "all" ? undefined : filter), listEmployees()])
      .then(([l, e]) => {
        setLeaves(l);
        setEmployees(e);
      })
      .finally(() => setLoading(false));
  };

  // useEffect(load, [filter]);

useEffect(() => {
  load();
}, [filter]);

  const employeeMap = Object.fromEntries(employees.map((e) => [e.id, e.name]));

  const handleAction = async (id, action) => {
    if (action === "approve") await approveLeave(id);
    else await rejectLeave(id);
    load();
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-serif text-lg text-ink">Leave Approvals</h2>
        <div className="flex gap-2">
          {["pending", "approved", "rejected", "all"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-card text-xs capitalize transition-colors ${
                filter === f ? "bg-ink text-white" : "bg-surface text-ink-muted border border-line"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-surface rounded-card shadow-card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-canvas text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">Employee</th>
              <th className="text-left px-5 py-3">From</th>
              <th className="text-left px-5 py-3">To</th>
              <th className="text-left px-5 py-3">Reason</th>
              <th className="text-left px-5 py-3">Status</th>
              <th className="text-right px-5 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={6} className="px-5 py-4 text-ink-muted">Loading…</td></tr>}
            {!loading && leaves.length === 0 && (
              <tr><td colSpan={6} className="px-5 py-4 text-ink-muted">No {filter !== "all" ? filter : ""} leave requests.</td></tr>
            )}
            {!loading && leaves.map((lv) => (
              <tr key={lv.id} className="border-t border-line">
                <td className="px-5 py-3 font-medium text-ink">{employeeMap[lv.employee_id] || `#${lv.employee_id}`}</td>
                <td className="px-5 py-3 font-mono text-xs">{lv.from_date}</td>
                <td className="px-5 py-3 font-mono text-xs">{lv.to_date}</td>
                <td className="px-5 py-3 text-ink-muted max-w-xs truncate">{lv.reason}</td>
                <td className="px-5 py-3">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${statusStyles[lv.status]}`}>
                    {lv.status}
                  </span>
                </td>
                <td className="px-5 py-3 text-right space-x-3">
                  {lv.status === "pending" && (
                    <>
                      <button onClick={() => handleAction(lv.id, "approve")} className="text-signal text-xs hover:underline">Approve</button>
                      <button onClick={() => handleAction(lv.id, "reject")} className="text-clay text-xs hover:underline">Reject</button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
