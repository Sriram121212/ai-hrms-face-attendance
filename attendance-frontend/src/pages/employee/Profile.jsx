import { useAuth } from "../../context/AuthContext";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="max-w-lg">
      <h2 className="font-serif text-lg text-ink mb-6">My Profile</h2>
      <div className="bg-surface rounded-card shadow-card p-6 space-y-4">
        <Row label="Name" value={user?.name} />
        <Row label="Employee ID" value={user?.employeeId} />
        <Row label="Role" value={user?.role} />
      </div>
      <p className="text-xs text-ink-muted mt-4">
        To update your details, contact an admin.
      </p>
    </div>
  );
}

function Row({ label, value }) {
  return (
    <div className="flex justify-between border-b border-line pb-3 last:border-0">
      <span className="text-ink-muted text-sm">{label}</span>
      <span className="text-ink text-sm font-medium capitalize">{value}</span>
    </div>
  );
}
