import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LiveClock from "../components/LiveClock";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await login(email, password);
      navigate(data.role === "admin" ? "/admin" : "/employee");
    } catch (err) {
      setError(
        err.response?.data?.detail === "Incorrect email or password"
          ? "That email or password doesn't match our records."
          : "Something went wrong. Try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-canvas">
      {/* Left panel - brand / signature moment */}
      <div className="hidden lg:flex flex-col justify-between bg-ink text-white p-12">
        <div>
          <p className="font-serif text-2xl">HRMS</p>
          <p className="text-white/50 text-sm mt-1 uppercase tracking-wider">Workforce &amp; Attendance</p>
        </div>

        <div>
          <p className="font-serif text-4xl leading-tight max-w-md">
            Every check-in, every shift, tracked the moment it happens.
          </p>
          <div className="mt-8 flex items-center gap-3 text-white/70">
            <span className="w-2.5 h-2.5 rounded-full bg-signal animate-pulse-dot" />
            <span className="font-mono text-sm">Live attendance ledger</span>
          </div>
        </div>

        <div className="font-mono text-xs">
          <LiveClock variant="dark" />
        </div>
      </div>

      {/* Right panel - login form */}
      <div className="flex items-center justify-center p-8">
        <form onSubmit={handleSubmit} className="w-full max-w-sm">
          <h1 className="font-serif text-2xl text-ink mb-1">Sign in</h1>
          <p className="text-ink-muted text-sm mb-8">Enter your work email and password.</p>

          {error && (
            <div className="mb-4 px-4 py-3 rounded-card bg-clay-soft text-clay text-sm">
              {error}
            </div>
          )}

          <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">
            Email
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@company.com"
            className="w-full px-4 py-2.5 mb-4 rounded-card border border-line bg-surface text-ink text-sm focus:border-ink outline-none transition-colors"
          />

          <label className="block text-xs uppercase tracking-wider text-ink-muted mb-1.5">
            Password
          </label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full px-4 py-2.5 mb-6 rounded-card border border-line bg-surface text-ink text-sm focus:border-ink outline-none transition-colors"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-ink text-white py-2.5 rounded-card text-sm font-medium hover:bg-ink-light transition-colors disabled:opacity-50"
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
