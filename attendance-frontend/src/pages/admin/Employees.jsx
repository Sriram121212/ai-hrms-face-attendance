import { useEffect, useState } from "react";
import { listEmployees, registerEmployee, deactivateEmployee } from "../../api/endpoints";

const emptyForm = {
  name: "",
  email: "",
  password: "",
  role: "employee",
  department: "",
  designation: "",
  join_date: "",
  base_salary: "",
  phone: "",
};

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    listEmployees()
      .then(setEmployees)
      .catch(() => setError("Couldn't load employees"))
      .finally(() => setLoading(false));
  };

  // useEffect(load, []);
useEffect(() => {
  load();
}, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await registerEmployee({ ...form, base_salary: Number(form.base_salary) });
      setForm(emptyForm);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not add employee");
    }
  };

  const handleDeactivate = async (id, name) => {
    if (!confirm(`Deactivate ${name}? Their history will be kept.`)) return;
    await deactivateEmployee(id);
    load();
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-serif text-lg text-ink">Employees</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-ink text-white px-4 py-2 rounded-card text-sm hover:bg-ink-light transition-colors"
        >
          {showForm ? "Cancel" : "+ Add Employee"}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-surface rounded-card shadow-card p-6 mb-6 grid grid-cols-2 gap-4"
        >
          {error && <p className="col-span-2 text-clay text-sm">{error}</p>}
          <Field label="Name" name="name" value={form.name} onChange={handleChange} required />
          <Field label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
          <Field label="Password" name="password" type="password" value={form.password} onChange={handleChange} required />
          <SelectField label="Role" name="role" value={form.role} onChange={handleChange} options={["employee", "admin"]} />
          <Field label="Department" name="department" value={form.department} onChange={handleChange} />
          <Field label="Designation" name="designation" value={form.designation} onChange={handleChange} />
          <Field label="Join Date" name="join_date" type="date" value={form.join_date} onChange={handleChange} required />
          <Field label="Base Salary" name="base_salary" type="number" value={form.base_salary} onChange={handleChange} required />
          <Field label="Phone" name="phone" value={form.phone} onChange={handleChange} />
          <div className="col-span-2">
            <button type="submit" className="bg-signal text-white px-5 py-2 rounded-card text-sm hover:opacity-90 transition-opacity">
              Save Employee
            </button>
          </div>
        </form>
      )}

      <div className="bg-surface rounded-card shadow-card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-canvas text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">Name</th>
              <th className="text-left px-5 py-3">Email</th>
              <th className="text-left px-5 py-3">Role</th>
              <th className="text-left px-5 py-3">Department</th>
              <th className="text-right px-5 py-3">Base Salary</th>
              <th className="text-right px-5 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={6} className="px-5 py-4 text-ink-muted">Loading…</td></tr>
            )}
            {!loading && employees.map((emp) => (
              <tr key={emp.id} className="border-t border-line">
                <td className="px-5 py-3 text-ink font-medium">{emp.name}</td>
                <td className="px-5 py-3 text-ink-muted">{emp.email}</td>
                <td className="px-5 py-3 capitalize">{emp.role}</td>
                <td className="px-5 py-3">{emp.department || "—"}</td>
                <td className="px-5 py-3 text-right font-mono">₹{emp.base_salary}</td>
                <td className="px-5 py-3 text-right">
                  <button
                    onClick={() => handleDeactivate(emp.id, emp.name)}
                    className="text-clay text-xs hover:underline"
                  >
                    Deactivate
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Field({ label, ...props }) {
  return (
    <div>
      <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">{label}</label>
      <input
        {...props}
        className="w-full px-3 py-2 rounded-card border border-line bg-surface text-ink text-sm focus:border-ink outline-none transition-colors"
      />
    </div>
  );
}

function SelectField({ label, options, ...props }) {
  return (
    <div>
      <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">{label}</label>
      <select
        {...props}
        className="w-full px-3 py-2 rounded-card border border-line bg-surface text-ink text-sm focus:border-ink outline-none transition-colors"
      >
        {options.map((o) => (
          <option key={o} value={o}>{o}</option>
        ))}
      </select>
    </div>
  );
}
