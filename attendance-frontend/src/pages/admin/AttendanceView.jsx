import { useEffect, useState } from "react";
import PresenceRibbon from "../../components/PresenceRibbon";
import { allAttendance, listEmployees } from "../../api/endpoints";

export default function AttendanceView() {
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listEmployees().then(setEmployees);
  }, []);

  useEffect(() => {
    setLoading(true);
    allAttendance(date)
      .then(setRecords)
      .finally(() => setLoading(false));
  }, [date]);

  const employeeMap = Object.fromEntries(employees.map((e) => [e.id, e.name]));

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-serif text-lg text-ink">Attendance</h2>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="px-3 py-2 rounded-card border border-line bg-surface text-sm font-mono"
        />
      </div>

      <div className="bg-surface rounded-card shadow-card p-6">
        {loading && <p className="text-sm text-ink-muted">Loading…</p>}
        {!loading && records.length === 0 && (
          <p className="text-sm text-ink-muted">No records for this date.</p>
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
