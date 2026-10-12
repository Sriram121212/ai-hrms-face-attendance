function timeToPercent(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  const hours = d.getHours() + d.getMinutes() / 60;
  return (hours / 24) * 100;
}

function formatTime(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

/**
 * A single employee's shift rendered as a horizontal ribbon against a 24-hour scale.
 * Filled segment = time between check-in and check-out.
 * A pulsing dot marks anyone still checked in (no check-out yet) — the "real-time" cue.
 */
export default function PresenceRibbon({ name, checkIn, checkOut, status }) {
  const startPct = timeToPercent(checkIn);
  const endPct = checkOut ? timeToPercent(checkOut) : timeToPercent(new Date().toISOString());
  const isActive = checkIn && !checkOut;

  const statusStyles = {
    present: "bg-signal-soft text-signal",
    absent: "bg-clay-soft text-clay",
    leave: "bg-amber-soft text-amber",
    half_day: "bg-amber-soft text-amber",
  };

  return (
    <div className="flex items-center gap-4 py-3 border-b border-line last:border-0">
      <div className="w-32 shrink-0">
        <p className="font-medium text-ink text-sm truncate">{name}</p>
        <span
          className={`inline-block mt-1 px-2 py-0.5 rounded text-[11px] font-medium ${
            statusStyles[status] || "bg-canvas text-ink-muted"
          }`}
        >
          {status?.replace("_", " ") || "no record"}
        </span>
      </div>

      <div className="flex-1 relative h-2.5 bg-canvas rounded-full overflow-visible">
        {startPct !== null && (
          <div
            className="absolute top-0 h-2.5 bg-signal rounded-full"
            style={{
              left: `${startPct}%`,
              width: `${Math.max(endPct - startPct, 1)}%`,
            }}
          />
        )}
        {isActive && startPct !== null && (
          <span
            className="absolute -top-[3px] w-3 h-3 rounded-full bg-signal animate-pulse-dot"
            style={{ left: `calc(${endPct}% - 6px)` }}
          />
        )}
      </div>

      <div className="w-28 shrink-0 text-right font-mono text-xs text-ink-muted">
        {formatTime(checkIn)} → {formatTime(checkOut)}
      </div>
    </div>
  );
}
