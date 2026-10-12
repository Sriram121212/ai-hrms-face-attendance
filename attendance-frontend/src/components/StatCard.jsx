export default function StatCard({ label, value, tone = "default" }) {
  const toneStyles = {
    default: "text-ink",
    signal: "text-signal",
    amber: "text-amber",
    clay: "text-clay",
  };

  return (
    <div className="bg-surface rounded-card shadow-card px-5 py-4 flex-1 min-w-[140px]">
      <p className="text-xs uppercase tracking-wider text-ink-muted mb-1">{label}</p>
      <p className={`font-serif text-3xl ${toneStyles[tone]}`}>{value}</p>
    </div>
  );
}
