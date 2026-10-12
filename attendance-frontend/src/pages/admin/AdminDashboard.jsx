import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import PresenceRibbon from "../../components/PresenceRibbon";
import { allAttendance, listEmployees, allLeaves } from "../../api/endpoints";

export default function AdminDashboard() {
  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [pendingLeaves, setPendingLeaves] = useState(0);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const today = new Date().toISOString().slice(0, 10);

    Promise.all([allAttendance(today), listEmployees(), allLeaves("pending")])
      .then(([att, emp, leaves]) => {
        setRecords(att);
        setEmployees(emp);
        setPendingLeaves(leaves.length);
      })
      .catch(() => setErrorMsg("Couldn't load today's data. Check that the backend is running."))
      .finally(() => setLoading(false));
  }, []);

  const presentCount = records.filter((r) => r.status === "present").length;
  const absentCount = employees.length - presentCount;

  // Build a lookup so we can show employee names alongside attendance rows
  const employeeMap = Object.fromEntries(employees.map((e) => [e.id, e.name]));

  return (
    <div>
      <div className="flex gap-4 mb-8 flex-wrap">
        <StatCard label="Total Employees" value={employees.length} />
        <StatCard label="Present Today" value={presentCount} tone="signal" />
        <StatCard label="Absent Today" value={Math.max(absentCount, 0)} tone="clay" />
        <StatCard label="Pending Leaves" value={pendingLeaves} tone="amber" />
      </div>

      <div className="bg-surface rounded-card shadow-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-serif text-lg text-ink">Today's Presence</h2>
          <span className="text-xs text-ink-muted font-mono">00:00 — 24:00</span>
        </div>

        {loading && <p className="text-sm text-ink-muted">Loading…</p>}
        {errorMsg && <p className="text-sm text-clay">{errorMsg}</p>}

        {!loading && !errorMsg && records.length === 0 && (
          <p className="text-sm text-ink-muted">No attendance recorded yet today.</p>
        )}

        {!loading &&
          records.map((r) => (
            <PresenceRibbon
              key={r.id}
              name={employeeMap[r.employee_id] || `Employee #${r.employee_id}`}
              checkIn={r.check_in_time}
              checkOut={r.check_out_time}
              status={r.status}
            />
          ))}
      </div>
    </div>
  );
}
